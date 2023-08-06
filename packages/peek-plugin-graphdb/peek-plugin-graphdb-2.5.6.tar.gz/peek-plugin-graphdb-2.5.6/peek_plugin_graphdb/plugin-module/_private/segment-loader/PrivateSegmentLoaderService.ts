import {Injectable} from "@angular/core";

import {
    ComponentLifecycleEventEmitter,
    extend,
    Payload,
    PayloadEnvelope,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    TupleSelector,
    TupleStorageFactoryService,
    VortexService,
    VortexStatusService
} from "@synerty/vortexjs";

import {graphDbCacheStorageName, graphDbFilt, graphDbTuplePrefix} from "../PluginNames";


import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import {EncodedSegmentChunkTuple} from "./EncodedSegmentChunkTuple";
import {SegmentIndexUpdateDateTuple} from "./SegmentIndexUpdateDateTuple";
import {GraphDbLinkedSegment} from "../../GraphDbLinkedSegment";
import {GraphDbTupleService} from "../GraphDbTupleService";
import {PrivateSegmentLoaderStatusTuple} from "./PrivateSegmentLoaderStatusTuple";

import {OfflineConfigTuple} from "../tuples/OfflineConfigTuple";
import {GraphDbPackedSegmentTuple} from "./GraphDbPackedSegmentTuple";

// ----------------------------------------------------------------------------

export interface SegmentResultI {
    [key: string]: GraphDbLinkedSegment
}

// ----------------------------------------------------------------------------

let clientSegmentWatchUpdateFromDeviceFilt = extend(
    {'key': "clientSegmentWatchUpdateFromDevice"},
    graphDbFilt
);

const cacheAll = "cacheAll";

// ----------------------------------------------------------------------------
/** SegmentChunkTupleSelector
 *
 * This is just a short cut for the tuple selector
 */

class SegmentChunkTupleSelector extends TupleSelector {

    constructor(private chunkKey: string) {
        super(graphDbTuplePrefix + "SegmentChunkTuple", {key: chunkKey});
    }

    toOrderedJsonStr(): string {
        return this.chunkKey;
    }
}

// ----------------------------------------------------------------------------
/** UpdateDateTupleSelector
 *
 * This is just a short cut for the tuple selector
 */
class UpdateDateTupleSelector extends TupleSelector {
    constructor() {
        super(SegmentIndexUpdateDateTuple.tupleName, {});
    }
}


// ----------------------------------------------------------------------------
/** hash method
 */
let BUCKET_COUNT = 8192;

function keyChunk(modelSetKey: string, key: string): string {
    /** Object ID Chunk

     This method creates an int from 0 to MAX, representing the hash bucket for this
     object Id.

     This is simple, and provides a reasonable distribution

     @param modelSetKey: The key of the model set that the segments are in
     @param key: The key of the segment to get the chunk key for

     @return: The bucket / chunkKey where you'll find the object with this ID

     */
    if (key == null || key.length == 0)
        throw new Error("key is None or zero length");

    let bucket = 0;

    for (let i = 0; i < key.length; i++) {
        bucket = ((bucket << 5) - bucket) + key.charCodeAt(i);
        bucket |= 0; // Convert to 32bit integer
    }

    bucket = bucket & (BUCKET_COUNT - 1);

    return `${modelSetKey}.${bucket}`;
}


// ----------------------------------------------------------------------------
/** Segment Cache
 *
 * This class has the following responsibilities:
 *
 * 1) Maintain a local storage-old of the index
 *
 * 2) Return DispKey graphDbs based on the index.
 *
 */
@Injectable()
export class PrivateSegmentLoaderService extends ComponentLifecycleEventEmitter {
    private UPDATE_CHUNK_FETCH_SIZE = 10;
    private OFFLINE_CHECK_PERIOD_MS = 15 * 60 * 1000; // 15 minutes

    private index = new SegmentIndexUpdateDateTuple();
    private askServerChunks: SegmentIndexUpdateDateTuple[] = [];

    private _hasLoaded = false;

    private _hasLoadedSubject = new Subject<void>();
    private storage: TupleOfflineStorageService;

    private _statusSubject = new Subject<PrivateSegmentLoaderStatusTuple>();
    private _status = new PrivateSegmentLoaderStatusTuple();

    private offlineConfig: OfflineConfigTuple = new OfflineConfigTuple();


    constructor(private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                storageFactory: TupleStorageFactoryService,
                private tupleService: GraphDbTupleService) {
        super();

        this.tupleService.offlineObserver
            .subscribeToTupleSelector(new TupleSelector(OfflineConfigTuple.tupleName, {}),
                false, false, true)
            .takeUntil(this.onDestroyEvent)
            .filter(v => v.length != 0)
            .subscribe((tuples: OfflineConfigTuple[]) => {
                this.offlineConfig = tuples[0];
                if (this.offlineConfig.cacheChunksForOffline)
                    this.initialLoad();
                this._notifyStatus();
            });

        this.storage = new TupleOfflineStorageService(
            storageFactory,
            new TupleOfflineStorageNameService(graphDbCacheStorageName)
        );

        this.setupVortexSubscriptions();
        this._notifyStatus();

        // Check for updates every so often
        Observable.interval(this.OFFLINE_CHECK_PERIOD_MS)
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this.askServerForUpdates());
    }

    isReady(): boolean {
        return this._hasLoaded;
    }

    isReadyObservable(): Observable<void> {
        return this._hasLoadedSubject;
    }

    statusObservable(): Observable<PrivateSegmentLoaderStatusTuple> {
        return this._statusSubject;
    }

    status(): PrivateSegmentLoaderStatusTuple {
        return this._status;
    }

    private _notifyReady(): void {
        if (this._hasLoaded)
            this._hasLoadedSubject.next();
    }

    private _notifyStatus(): void {
        this._status.cacheForOfflineEnabled = this.offlineConfig.cacheChunksForOffline;
        this._status.initialLoadComplete = this.index.initialLoadComplete;

        this._status.loadProgress = Object.keys(this.index.updateDateByChunkKey).length;
        for (let chunk of this.askServerChunks)
            this._status.loadProgress -= Object.keys(chunk.updateDateByChunkKey).length;

        this._statusSubject.next(this._status);
    }

    /** Initial load
     *
     * Load the dates of the index buckets and ask the server if it has any updates.
     */
    private initialLoad(): void {

        this.storage.loadTuples(new UpdateDateTupleSelector())
            .then((tuplesAny: any[]) => {
                let tuples: SegmentIndexUpdateDateTuple[] = tuplesAny;
                if (tuples.length != 0) {
                    this.index = tuples[0];

                    if (this.index.initialLoadComplete) {
                        this._hasLoaded = true;
                        this._notifyReady();
                    }

                }

                this.askServerForUpdates();
                this._notifyStatus();
            });

        this._notifyStatus();
    }

    private setupVortexSubscriptions(): void {

        // Services don't have destructors, I'm not sure how to unsubscribe.
        this.vortexService
            .createEndpointObservable(this, clientSegmentWatchUpdateFromDeviceFilt)
            .takeUntil(this.onDestroyEvent)
            .subscribe((payloadEnvelope: PayloadEnvelope) => {
                this.processSegmentsFromServer(payloadEnvelope);
            });

        // If the vortex service comes back online, update the watch grids.
        this.vortexStatusService.isOnline
            .filter(isOnline => isOnline == true)
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this.askServerForUpdates());

    }

    private areWeTalkingToTheServer(): boolean {
        return this.offlineConfig.cacheChunksForOffline
            && this.vortexStatusService.snapshot.isOnline;
    }


    /** Ask Server For Updates
     *
     * Tell the server the state of the chunks in our index and ask if there
     * are updates.
     *
     */
    private askServerForUpdates() {
        if (!this.areWeTalkingToTheServer()) return;

        // If we're still caching, then exit
        if (this.askServerChunks.length != 0) {
            this.askServerForNextUpdateChunk();
            return;
        }

        this.tupleService.observer
            .pollForTuples(new UpdateDateTupleSelector())
            .then((tuplesAny: any) => {
                let serverIndex: SegmentIndexUpdateDateTuple = tuplesAny[0];
                let keys = Object.keys(serverIndex.updateDateByChunkKey);
                let keysNeedingUpdate: string[] = [];

                this._status.loadTotal = keys.length;

                // Tuples is an array of strings
                for (let chunkKey of keys) {
                    if (!this.index.updateDateByChunkKey.hasOwnProperty(chunkKey)) {
                        this.index.updateDateByChunkKey[chunkKey] = null;
                        keysNeedingUpdate.push(chunkKey);

                    } else if (this.index.updateDateByChunkKey[chunkKey]
                        != serverIndex.updateDateByChunkKey[chunkKey]) {
                        keysNeedingUpdate.push(chunkKey);
                    }
                }
                this.queueChunksToAskServer(keysNeedingUpdate);
            });
    }


    /** Queue Chunks To Ask Server
     *
     */
    private queueChunksToAskServer(keysNeedingUpdate: string[]) {
        if (!this.areWeTalkingToTheServer()) return;

        this.askServerChunks = [];

        let count = 0;
        let indexChunk = new SegmentIndexUpdateDateTuple();

        for (let key of keysNeedingUpdate) {
            indexChunk.updateDateByChunkKey[key] = this.index.updateDateByChunkKey[key];
            count++;

            if (count == this.UPDATE_CHUNK_FETCH_SIZE) {
                this.askServerChunks.push(indexChunk);
                count = 0;
                indexChunk = new SegmentIndexUpdateDateTuple();
            }
        }

        if (count)
            this.askServerChunks.push(indexChunk);

        this.askServerForNextUpdateChunk();

        this._status.lastCheck = new Date();
    }

    private askServerForNextUpdateChunk() {
        if (!this.areWeTalkingToTheServer()) return;

        if (this.askServerChunks.length == 0)
            return;

        let indexChunk: SegmentIndexUpdateDateTuple = this.askServerChunks.pop();
        let filt = extend({}, clientSegmentWatchUpdateFromDeviceFilt);
        filt[cacheAll] = true;
        let pl = new Payload(filt, [indexChunk]);
        this.vortexService.sendPayload(pl);

        this._status.lastCheck = new Date();
        this._notifyStatus();
    }


    /** Process Segmentes From Server
     *
     * Process the grids the server has sent us.
     */
    private processSegmentsFromServer(payloadEnvelope: PayloadEnvelope) {

        if (payloadEnvelope.result != null && payloadEnvelope.result != true) {
            console.log(`ERROR: ${payloadEnvelope.result}`);
            return;
        }

        payloadEnvelope
            .decodePayload()
            .then((payload: Payload) => this.storeSegmentPayload(payload))
            .then(() => {
                if (this.askServerChunks.length == 0) {
                    this.index.initialLoadComplete = true;
                    this._hasLoaded = true;
                    this._hasLoadedSubject.next();

                } else if (payloadEnvelope.filt[cacheAll] == true) {
                    this.askServerForNextUpdateChunk();

                }

            })
            .then(() => this._notifyStatus())
            .catch(e =>
                `SegmentCache.processSegmentsFromServer failed: ${e}`
            );

    }

    private storeSegmentPayload(payload: Payload) {

        let tuplesToSave: EncodedSegmentChunkTuple[] = <EncodedSegmentChunkTuple[]>payload.tuples;
        if (tuplesToSave.length == 0)
            return;

        // 2) Store the index
        this.storeSegmentChunkTuples(tuplesToSave)
            .then(() => {
                // 3) Store the update date

                for (let graphDbIndex of tuplesToSave) {
                    this.index.updateDateByChunkKey[graphDbIndex.chunkKey] = graphDbIndex.lastUpdate;
                }

                return this.storage.saveTuples(
                    new UpdateDateTupleSelector(), [this.index]
                );

            })
            .catch(e => console.log(
                `SegmentCache.storeSegmentPayload: ${e}`));

    }

    /** Store Index Bucket
     * Stores the index bucket in the local db.
     */
    private storeSegmentChunkTuples(encodedSegmentChunkTuples: EncodedSegmentChunkTuple[]): Promise<void> {
        let retPromise: any;
        retPromise = this.storage.transaction(true)
            .then((tx) => {

                let promises = [];

                for (let encodedSegmentChunkTuple of encodedSegmentChunkTuples) {
                    promises.push(
                        tx.saveTuplesEncoded(
                            new SegmentChunkTupleSelector(encodedSegmentChunkTuple.chunkKey),
                            encodedSegmentChunkTuple.encodedData
                        )
                    );
                }

                return Promise.all(promises)
                    .then(() => tx.close());
            });
        return retPromise;
    }


    /** Get Segments
     *
     * Get the objects with matching keywords from the index..
     *
     */
    getSegments(modelSetKey: string, keys: string[]): Promise<SegmentResultI> {
        if (keys == null || keys.length == 0) {
            throw new Error("We've been passed a null/empty keys");
        }

        if (!this.offlineConfig.cacheChunksForOffline) {
            let ts = new TupleSelector(GraphDbPackedSegmentTuple.tupleName, {
                "modelSetKey": modelSetKey,
                "keys": keys
            });

            let isOnlinePromise: any = this.vortexStatusService.snapshot.isOnline ?
                Promise.resolve() :
                this.vortexStatusService.isOnline
                    .filter(online => online)
                    .first()
                    .toPromise();

            return isOnlinePromise
                .then(() => this.tupleService.offlineObserver.pollForTuples(ts, false))
                .then((packedSegments:GraphDbPackedSegmentTuple[]) => {
                    let linkedSegments = [];
                    for (let packed of packedSegments) {
                        // Create the new object
                        let newObject = new GraphDbLinkedSegment();
                        newObject.unpackJson(packed.packedJson, packed.key, modelSetKey);
                        linkedSegments.push(newObject);
                    }
                    return linkedSegments;
                })
                .then((segments: GraphDbLinkedSegment[]) => this._makeDictFromSegments(segments));
        }

        if (this.isReady())
            return this.getSegmentsWhenReady(modelSetKey, keys)
                .then(segments => this._makeDictFromSegments(segments));

        return this.isReadyObservable()
            .first()
            .toPromise()
            .then(() => this.getSegmentsWhenReady(modelSetKey, keys))
            .then(segments => this._makeDictFromSegments(segments));
    }


    /** Get Segments When Ready
     *
     * Get the objects with matching keywords from the index..
     *
     */
    private getSegmentsWhenReady(
        modelSetKey: string, keys: string[]): Promise<GraphDbLinkedSegment[]> {

        let keysByChunkKey: { [key: string]: string[]; } = {};
        let chunkKeys: string[] = [];

        for (let key of keys) {
            let chunkKey: string = keyChunk(modelSetKey, key);
            if (keysByChunkKey[chunkKey] == null)
                keysByChunkKey[chunkKey] = [];
            keysByChunkKey[chunkKey].push(key);
            chunkKeys.push(chunkKey);
        }


        let promises = [];
        for (let chunkKey of chunkKeys) {
            let keysForThisChunk = keysByChunkKey[chunkKey];
            promises.push(
                this.getSegmentsForKeys(modelSetKey, keysForThisChunk, chunkKey)
            );
        }

        return Promise.all(promises)
            .then((promiseResults: GraphDbLinkedSegment[][]) => {
                let objects: GraphDbLinkedSegment[] = [];
                for (let results of  promiseResults) {
                    for (let result of results) {
                        objects.push(result);
                    }
                }
                return objects;
            });
    }


    /** Get Segments for Object ID
     *
     * Get the objects with matching keywords from the index..
     *
     */
    private getSegmentsForKeys(modelSetKey: string,
                               keys: string[],
                               chunkKey: string): Promise<GraphDbLinkedSegment[]> {

        if (!this.index.updateDateByChunkKey.hasOwnProperty(chunkKey)) {
            console.log(`ObjectIDs: ${keys} doesn't appear in the index`);
            return Promise.resolve([]);
        }

        let retPromise: any;
        retPromise = this.storage.loadTuplesEncoded(new SegmentChunkTupleSelector(chunkKey))
            .then((vortexMsg: string) => {
                if (vortexMsg == null) {
                    return [];
                }


                return Payload.fromEncodedPayload(vortexMsg)
                    .then((payload: Payload) => JSON.parse(<any>payload.tuples))
                    .then((chunkData: { [key: number]: string; }) => {

                        let foundSegments: GraphDbLinkedSegment[] = [];

                        for (let key of keys) {
                            // Find the keyword, we're just iterating
                            if (!chunkData.hasOwnProperty(key)) {
                                console.log(
                                    `WARNING: Segment ${key} is missing from index,`
                                    + ` chunkKey ${chunkKey}`
                                );
                                continue;
                            }

                            // Create the new object
                            let newObject = new GraphDbLinkedSegment();
                            newObject.unpackJson(chunkData[key], key, modelSetKey);
                            foundSegments.push(newObject);

                        }

                        return foundSegments;

                    });
            });

        return retPromise;

    }

    private _makeDictFromSegments(segments: GraphDbLinkedSegment[]): SegmentResultI {

        let objects: { [key: string]: GraphDbLinkedSegment } = {};
        for (let doc of  segments) {
            objects[doc.key] = doc;
        }
        return objects;
    }


}