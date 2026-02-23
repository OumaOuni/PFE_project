sap.ui.define(["sap/m/MessageToast"], function (MessageToast) {
  "use strict";

  return {
    login: function (oEvent) {
      var oModel = oEvent.getSource().getParent().getModel();
      var username = oModel.getProperty("/username");
      var password = oModel.getProperty("/password");

      fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.role === "ceo") {
            window.location.href = "dashboard_ceo.html";
          } else if (data.role === "sales_manager") {
            window.location.href = "dashboard_sales.html";
          } else if (data.role === "inventory_manager") {
            window.location.href = "dashboard_inventory.html";
          }
        })
        .catch((err) => MessageToast.show("Login failed"));
    },
  };
});
