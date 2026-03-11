sap.ui.define(
  ["sap/ui/core/mvc/Controller", "sap/ui/model/json/JSONModel", "sap/m/MessageBox"],
  function (Controller, JSONModel, MessageBox) {
    "use strict";

    return Controller.extend("myApp.controller.InventoryDashboard", {
      onInit: function () {
        var oModel = new JSONModel({
          summary: {},
          critical_stock: [],
          low_stock: [],
          stock_by_category: [],
          movements: [],
          all_products: [],
        });
        this.getView().setModel(oModel, "invModel");
        this._loadDashboard();
      },

      _loadDashboard: function () {
        var sToken = sessionStorage.getItem("token");
        var oModel = this.getView().getModel("invModel");

        fetch("http://localhost:8000/dashboard/inventory", {
          method: "GET",
          headers: {
            Authorization: "Bearer " + sToken,
            "Content-Type": "application/json",
          },
        })
          .then(function (response) {
            if (!response.ok) {
              throw new Error("Failed to load inventory data");
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
