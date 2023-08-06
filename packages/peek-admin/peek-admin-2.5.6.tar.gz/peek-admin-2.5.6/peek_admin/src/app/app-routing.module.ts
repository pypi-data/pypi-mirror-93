import { NgModule } from "@angular/core"
import { Route, RouterModule, Routes } from "@angular/router"
import { DashboardComponent } from "./dashboard/dashboard.component"
import { Tuple } from "@synerty/vortexjs"
import { pluginAppRoutes } from "../plugin-app-routes"
import { pluginCfgRoutes } from "../plugin-cfg-routes"

export const dashboardRoute: Route = {
    path: "",
    component: DashboardComponent
}

const staticRoutes: Routes = [
    dashboardRoute,
    // environmentRoute,
    {
        path: "**",
        component: DashboardComponent
    }
]

class PluginRoutesTuple extends Tuple {
    pluginName: string
    lazyLoadModulePath: string

    constructor() {
        super("peek_server.PluginRoutesTuple")
    }
}

@NgModule({
    imports: [
        RouterModule.forRoot([
            ...pluginAppRoutes,
            ...pluginCfgRoutes,
            ...staticRoutes
        ])
    ],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
