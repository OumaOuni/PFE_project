sap.ui.define(
  [
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/ui/model/Filter",
    "sap/m/MessageToast",
    "sap/m/MessageBox",
  ],
  function (Controller, JSONModel, Filter, MessageToast, MessageBox) {
    "use strict";

    return Controller.extend("myApp.controller.ADMINDashboard", {
      onInit: function () {
        var oUserModel = new JSONModel();
        this.getView().setModel(oUserModel, "userModel");
        this.fetchUsers();
      },

      fetchUsers: async function () {
        try {
          const token = sessionStorage.getItem("token");
          if (!token) {
            MessageToast.show("Authentication required. Please login again.");
            return;
          }

          const response = await fetch("http://127.0.0.1:8000/admin/users", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const users = await response.json();
            const oUserModel = this.getView().getModel("userModel");
            oUserModel.setProperty("/users", users);
          } else if (response.status === 401) {
            MessageToast.show("Session expired. Please login again.");
          } else {
            const errorData = await response.json();
            MessageToast.show(
              "Failed to load users: " + (errorData.detail || "Unknown error"),
            );
          }
        } catch (error) {
          MessageToast.show("Network error: " + error.message);
          console.error("Error fetching users:", error);
        }
      },

      onOpenAddUserDialog: function () {
        this.byId("addUserDialog").open();
      },
      onCancelAddUser: function () {
        this.byId("addUserDialog").close();
      },
      onValidateInputs: function () {
        const username = this.byId("usernameInput").getValue().trim();
        const email = this.byId("emailInput").getValue().trim();
        const password = this.byId("passwordInput").getValue().trim();
        const role = this.byId("roleInput").getSelectedKey().trim();
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        let isValid = true;

        if (email.length > 0 && !emailRegex.test(email)) {
          this.byId("emailInput").setValueState("Error");
          this.byId("emailInput").setValueStateText(
            "Enter a valid email address",
          );
          isValid = false;
        } else {
          this.byId("emailInput").setValueState("None");
          this.byId("emailInput").setValueStateText("");
        }

        isValid =
          isValid &&
          username.length > 0 &&
          email.length > 0 &&
          password.length > 0 &&
          role.length > 0;

        this.byId("addUserBtn").setEnabled(isValid);
      },
      onAddUser: async function () {
        const username = this.byId("usernameInput").getValue();
        const email = this.byId("emailInput").getValue();
        const password = this.byId("passwordInput").getValue();
        const role = this.byId("roleInput").getSelectedKey();
        const token = sessionStorage.getItem("token");

        try {
          const response = await fetch("http://127.0.0.1:8000/admin/users", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ username, email, password, role }),
          });

          if (response.ok) {
            sap.m.MessageToast.show("User added successfully");
            this.byId("addUserDialog").close();
            this.byId("usernameInput").setValue("");
            this.byId("emailInput").setValue("");
            this.byId("passwordInput").setValue("");
            this.byId("roleInput").setSelectedKey("");
            this.fetchUsers();
          } else {
            const errorData = await response.json();
            sap.m.MessageToast.show(errorData.detail || "Failed to add user");
            this.byId("emailInput").setValueState("Error");
            this.byId("emailInput").setValueStateText(errorData.detail);
          }
        } catch (error) {
          sap.m.MessageToast.show("Network error: " + error.message);
          console.error(error);
        }
      },

      onOpenEditUserDialog: function (oEvent) {
        const oItem = oEvent.getSource().getParent().getParent();
        const oContext = oItem.getBindingContext("userModel");
        if (!oContext) {
          MessageToast.show("Please select a user to edit");
          return;
        }
        const oEditDialog = this.byId("editUserDialog");
        oEditDialog.setBindingContext(oContext, "userModel");
        oEditDialog.open();
      },
      onCancelEditUser: function () {
        this.byId("editUserDialog").close();
      },
      onConfirmEditUser: async function () {
        const oContext =
          this.byId("editUserDialog").getBindingContext("userModel");
        const user = oContext.getObject();
        const token = sessionStorage.getItem("token");

        try {
          const username = this.byId("editUserDialog")
            .getContent()[0]
            .getItems()[0]
            .getValue();
          const email = this.byId("editUserDialog")
            .getContent()[0]
            .getItems()[1]
            .getValue();
          const password = this.byId("editPasswordInput").getValue();
          const role = this.byId("editUserDialog")
            .getContent()[0]
            .getItems()[3]
            .getSelectedKey();

          const payload = {
            username: username || user.username,
            email: email || user.email,
            role: role || user.role,
          };

          if (password && password.trim() !== "") {
            payload.password = password;
          }

          const response = await fetch(
            `http://127.0.0.1:8000/admin/users/${user.id}`,
            {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify(payload),
            },
          );

          if (response.ok) {
            MessageToast.show("User updated successfully");
            this.byId("editUserDialog").close();
            this.fetchUsers();
          } else {
            const errorData = await response.json();
            MessageToast.show(errorData.detail || "Failed to update user");
          }
        } catch (err) {
          console.error("Failed to edit user:", err);
          MessageToast.show("Network error: " + err.message);
        }
      },
      onUserSelectionChange: function (oEvent) {
        var aSelectedItems = oEvent.getSource().getSelectedItems();
        this.byId("editUserBtn") &&
          this.byId("editUserBtn").setEnabled(aSelectedItems.length > 0);
        this.byId("deleteUserBtn") &&
          this.byId("deleteUserBtn").setEnabled(aSelectedItems.length > 0);
      },
      onDeleteUser: function (oEvent) {
        const oItem = oEvent.getSource().getParent().getParent();
        const oContext = oItem.getBindingContext("userModel");
        if (!oContext) {
          MessageToast.show("Please select a user to delete");
          return;
        }
        const user = oContext.getObject();
        this.confirmAndDeleteUser([user]);
      },
      onDeleteSelectedUser: function () {
        const oTable = this.byId("usersTable");
        const aSelectedItems = oTable.getSelectedItems();

        if (aSelectedItems.length === 0) {
          MessageToast.show("Please select user(s) to delete");
          return;
        }

        const aUsers = aSelectedItems.map((item) =>
          item.getBindingContext("userModel").getObject(),
        );

        this.confirmAndDeleteUser(aUsers);
      },
      confirmAndDeleteUser: function (aUsers) {
        const iCount = aUsers.length;
        const userNames = aUsers.map((u) => u.username).join(", ");
        const message =
          iCount === 1
            ? `Delete user: ${userNames}?`
            : `Delete ${iCount} users: ${userNames}?`;

        MessageBox.confirm(message, {
          onClose: (sAction) => {
            if (sAction === MessageBox.Action.OK) {
              this.deleteMultipleUsers(aUsers.map((u) => u.id));
            }
          },
        });
      },
      deleteMultipleUsers: async function (aUserIds) {
        const token = sessionStorage.getItem("token");
        let successCount = 0;
        let failCount = 0;

        for (const userId of aUserIds) {
          try {
            const response = await fetch(
              `http://127.0.0.1:8000/admin/users/${userId}`,
              {
                method: "DELETE",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              },
            );

            if (response.ok) {
              successCount++;
            } else {
              failCount++;
            }
          } catch (err) {
            failCount++;
            console.error("Failed to delete user:", err);
          }
        }

        if (successCount > 0) {
          MessageToast.show(`${successCount} user(s) deleted successfully`);
          this.fetchUsers();
        }
        if (failCount > 0) {
          MessageToast.show(`Failed to delete ${failCount} user(s)`);
        }
      },
      onSearchUsers: function (oEvent) {
        const sQuery = oEvent.getSource().getValue().toLowerCase();
        const oTable = this.byId("usersTable");
        const oBinding = oTable.getBinding("items");

        if (sQuery === "") {
          oBinding.filter([]);
        } else {
          const aFilter = [
            new Filter("username", "Contains", sQuery),
            new Filter("email", "Contains", sQuery),
          ];
          const oMultiFilter = new Filter(aFilter, false);
          oBinding.filter([oMultiFilter]);
        }
      },
    });
  },
);
