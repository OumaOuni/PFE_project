sap.ui.define(["sap/ui/core/mvc/Controller"], function (Controller) {
  "use strict";

  return Controller.extend("myApp.controller.SalesDashboard", {
    onInit: function () {
      console.log("Sales Dashboard loaded");
    },
  });
});
