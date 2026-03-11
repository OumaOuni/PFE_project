sap.ui.define(
  ["sap/ui/core/UIComponent", "sap/ui/Device"],
  function (UIComponent, Device) {
    "use strict";

    return UIComponent.extend("myApp.Component", {
      metadata: {
        manifest: "json",
      },

      init: function () {
        UIComponent.prototype.init.apply(this, arguments);

        // Initialize router
        var oRouter = this.getRouter();
        oRouter.attachRouteMatched(this._onRouteMatched, this);
        oRouter.initialize();
      },

      _onRouteMatched: function (oEvent) {
        var sRouteName = oEvent.getParameter("name");

        var sToken = sessionStorage.getItem("token");
        var sRole = sessionStorage.getItem("role");

        // If not logged in → force login
        if (!sToken && sRouteName !== "Login") {
          this.getRouter().navTo("Login");
          return;
        }

        // Role protection map
        var roleMap = {
          CEODashboard: "ceo",
          SalesDashboard: "sales_manager",
          InventoryDashboard: "inventory_manager",
          ADMINDashboard: "admin",
        };

        if (roleMap[sRouteName] && roleMap[sRouteName] !== sRole) {
          this.getRouter().navTo("Login");
        }
      },
    });
  },
);
