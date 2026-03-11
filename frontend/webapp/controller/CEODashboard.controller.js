sap.ui.define(
  ["sap/ui/core/mvc/Controller", "sap/ui/model/json/JSONModel", "sap/m/MessageBox"],
  function (Controller, JSONModel, MessageBox) {
    "use strict";

    return Controller.extend("myApp.controller.CEODashboard", {
      onInit: function () {
        var oModel = new JSONModel({
          kpis: {},
          monthly_trend: [],
          sales_by_region: [],
          top_products: [],
          low_stock: [],
        });
        this.getView().setModel(oModel, "ceoModel");
        this._loadDashboard();
      },

      _loadDashboard: function () {
        var sToken = sessionStorage.getItem("token");
        var oModel = this.getView().getModel("ceoModel");

        fetch("http://localhost:8000/dashboard/ceo", {
          method: "GET",
          headers: {
            Authorization: "Bearer " + sToken,
            "Content-Type": "application/json",
          },
        })
          .then(function (response) {
            if (!response.ok) {
              throw new Error("Failed to load CEO data");
            }
            return response.json();
          })
          .then(function (data) {
            oModel.setData(data);
          })
          .catch(function (err) {
            MessageBox.error("Could not load dashboard data: " + err.message);
          });
      },

      onLogout: function () {
        sessionStorage.clear();
        this.getOwnerComponent().getRouter().navTo("Login");
      },
    });
  },
);
