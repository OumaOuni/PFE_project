sap.ui.define(
  ["sap/ui/core/mvc/Controller", "sap/ui/model/json/JSONModel", "sap/m/MessageBox"],
  function (Controller, JSONModel, MessageBox) {
    "use strict";

    return Controller.extend("myApp.controller.SalesDashboard", {
      onInit: function () {
        var oModel = new JSONModel({
          leaderboard: [],
          sales_by_category: [],
          monthly_vs_target: [],
          top_customers: [],
          sales_by_city: [],
          avg_order_value: 0,
        });
        this.getView().setModel(oModel, "salesModel");
        this._loadDashboard();
      },

      _loadDashboard: function () {
        var sToken = sessionStorage.getItem("token");
        var oModel = this.getView().getModel("salesModel");

        fetch("http://localhost:8000/dashboard/sales", {
          method: "GET",
          headers: {
            Authorization: "Bearer " + sToken,
            "Content-Type": "application/json",
          },
        })
          .then(function (response) {
            if (!response.ok) {
              throw new Error("Failed to load sales data");
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
