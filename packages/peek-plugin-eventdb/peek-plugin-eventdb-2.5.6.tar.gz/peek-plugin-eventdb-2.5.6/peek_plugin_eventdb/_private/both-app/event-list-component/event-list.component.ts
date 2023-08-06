import {Component, Input, OnInit} from "@angular/core";
import {PrivateEventDBService} from "@peek/peek_plugin_eventdb/_private/PrivateEventDBService";
import {EventDBEventTuple, EventDBPropertyTuple} from "@peek/peek_plugin_eventdb/tuples";
import {DocDbPopupService, DocDbPopupTypeE} from "@peek/peek_plugin_docdb";
import {eventdbPluginName} from "@peek/peek_plugin_eventdb/_private/PluginNames";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";
import {FilterI} from "../event-filter-component/event-filter.component";
import {ColumnI} from "../event-column-component/event-column.component";


@Component({
    selector: "plugin-eventdb-event-list",
    templateUrl: "event-list.component.web.html",
    styleUrls: ["../event-common.component.web.scss"],
    moduleId: module.id
})
export class EventDBEventListComponent extends ComponentLifecycleEventEmitter
    implements OnInit {

    @Input("modelSetKey")
    modelSetKey: string;

    private lastSubscription = null;
    private lastLoadFingerprint: string = "";

    colorsEnabled: boolean = false;

    events: EventDBEventTuple[] = [];
    props: EventDBPropertyTuple[] = [];
    displayProps: EventDBPropertyTuple[] = [];
    isDataLoading = true;

    constructor(private objectPopupService: DocDbPopupService,
                private eventService: PrivateEventDBService) {
        super();
    }

    ngOnInit() {
        this.eventService.propertyTuples(this.modelSetKey)
            .takeUntil(this.onDestroyEvent)
            .subscribe((props: EventDBPropertyTuple[]) => {
                // sort properties by order.
                this.props = props.sort((a, b) => a.order - b.order);
            });
    }

    updateColors(colorsOn: boolean): void {
        this.colorsEnabled = colorsOn;
    }

    updateColumn(props: ColumnI) {
        this.displayProps = props.selectedProps;
    }

    updateFilter(filter: FilterI) {
        // Create a string representing the last load
        const lastLoadFingerprint =
            this.eventService
                .eventTupleSelector(filter.modelSetKey,
                    filter.dateTimeRange, filter.criteria, filter.alarmsOnly)
                .toOrderedJsonStr();

        // If we have an active subscription and the fingerprint matches, do nothing
        if (lastLoadFingerprint == this.lastLoadFingerprint
            && this.lastSubscription != null) {
            return;
        }

        // record the fingerprint
        this.lastLoadFingerprint = lastLoadFingerprint;

        // Apply the update
        this.events = [];
        this.isDataLoading = true

        this.unsubUpdates();

        this.lastSubscription = this.eventService
            .eventTuples(filter.modelSetKey, filter.dateTimeRange,
                filter.criteria, filter.alarmsOnly)
            .subscribe((events: EventDBEventTuple[]) => {
                this.events = events;
                this.isDataLoading = false;
            });

    }

    private unsubUpdates() {
        if (this.lastSubscription != null)
            this.lastSubscription.unsubscribe();

        this.lastSubscription = null;
    }

    displayValue(event: EventDBEventTuple, prop: EventDBPropertyTuple): string {
        const eventVal = event.value[prop.key];
        return prop.values != null && prop.values.length != 0
            ? prop.rawValToUserVal(eventVal)
            : eventVal;
    }

    colorValue(event: EventDBEventTuple): string {
        if (!this.colorsEnabled)
            return null;

        // Stash this value here to improve performance
        if (event["color"] != null)
            return event["color"];

        let color = "";
        for (let prop of this.props) {
            const eventVal = event.value[prop.key];
            const thisColor = prop.rawValToColor(eventVal);
            if (thisColor != null) {
                color = thisColor;
                break;
            }
        }

        event["color"] = color;
        return color
    }

    private getDocDBPopupKey(event: EventDBEventTuple): string | null {
        for (let prop of this.props) {
            if (prop.useForPopup && event.value[prop.key] != null) {
                return event.value[prop.key];
            }
        }
        return null;
    }

    tooltipEnter($event: MouseEvent, result: EventDBEventTuple) {
        const docdbPopupKey = this.getDocDBPopupKey(result);
        if (docdbPopupKey == null)
            return;

        // const offset = $(".scroll-container").offset();
        this.objectPopupService
            .showPopup(
                false,
                DocDbPopupTypeE.tooltipPopup,
                eventdbPluginName,
                $event,
                this.modelSetKey,
                docdbPopupKey
            )
    }

    tooltipExit($event: MouseEvent, result: EventDBEventTuple) {
        this.objectPopupService.hidePopup(DocDbPopupTypeE.tooltipPopup);

    }

    showSummaryPopup($event: MouseEvent, result: EventDBEventTuple) {
        const docdbPopupKey = this.getDocDBPopupKey(result);
        if (docdbPopupKey == null)
            return;

        this.objectPopupService.hidePopup(DocDbPopupTypeE.tooltipPopup);
        this.objectPopupService
            .showPopup(
                true,
                DocDbPopupTypeE.summaryPopup,
                eventdbPluginName,
                $event,
                this.modelSetKey,
                docdbPopupKey
            )
    }

}
