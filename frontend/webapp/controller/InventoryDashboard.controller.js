sap.ui.define(["sap/ui/core/mvc/Controller"], function (Controller) {
  "use strict";

  return Controller.extend("myApp.controller.InventoryDashboard", {
    onInit: function () {
      console.log("Inventory Dashboard loaded");
    },
  });
});
