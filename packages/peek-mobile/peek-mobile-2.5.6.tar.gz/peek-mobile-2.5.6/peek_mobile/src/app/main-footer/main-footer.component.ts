import {Component} from "@angular/core";
import {
    IConfigLink,
    FooterService,
    NavBackService,
    TitleService
} from "@synerty/peek-plugin-base-js";
import {ComponentLifecycleEventEmitter, VortexStatusService} from "@synerty/vortexjs";

@Component({
    selector: "peek-main-footer",
    templateUrl: "main-footer.component.web.html",
    styleUrls: ["main-footer.component.web.scss"],
    moduleId: module.id
})
export class MainFooterComponent extends ComponentLifecycleEventEmitter {

    configLinks: IConfigLink[] = [];

    vortexIsOnline: boolean = false;
    statusText: string = "";
    isEnabled: boolean = true;

    constructor(vortexStatusService: VortexStatusService,
                footerService: FooterService,
                public navBackService: NavBackService,
                titleService: TitleService) {
        super();

        this.configLinks = footerService.configLinksSnapshot;

        footerService.statusText
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.statusText = v);

        titleService.isEnabled
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.isEnabled = v);

        this.configLinks = footerService.configLinksSnapshot;
        footerService.configLinks
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.configLinks = v);

        vortexStatusService.isOnline
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.vortexIsOnline = v);

    }

    isBackButtonEnabled(): boolean {
        return this.navBackService.navBackLen() != 0;
    }

    hasConfigLinks():boolean {
        return this.configLinks != null && this.configLinks.length != 0;
    }

}

