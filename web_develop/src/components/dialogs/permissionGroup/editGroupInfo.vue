<script>
export default {
  name: "EditGroupInfo",
  emits: ["success", "exit"],
  props: {
    openEditGroupStatusWindow: {
      type: Boolean,
      required: true
    },
    openEditGroupInfoWindow: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      editGroupStatus: {

      },
      editGroupInfo: {

      }
    }
  }
}
</script>

<template>
  <!--    修改权限组信息-->
  <v-dialog
    id="inputDialog"
    v-model="editPermissionGroupDialog.flag"
    activator="parent"
    min-width="400px"
    width="auto"
    persistent
  >
    <v-card>
      <v-card-title>编辑权限组--{{ editPermissionGroupDialog.name }}</v-card-title>
      <v-card-text>
        <v-text-field type="text" label="权限组名" v-model="editPermissionGroupDialog.name"></v-text-field>
        <v-switch label="是否启用" v-model="editPermissionGroupDialog.status" color="primary"></v-switch>
        <v-card class="pa-1">
          <v-card-title>请选择该组可使用的权限</v-card-title>
          <v-card-text>
            <v-table density="compact">
              <thead>
              <tr>
                <th class="text-left">
                  选择
                </th>
                <th class="text-left">
                  权限原名
                </th>
                <th class="text-left">
                  权限译名
                </th>
              </tr>
              </thead>
              <tbody>
              <tr
                v-for="(value, key) in editPermissionGroupDialog.permissionList"
                :key="key"
              >
                <td><input type="checkbox" :value="key" v-model="editPermissionGroupDialog.selected"></td>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
              </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-card-text>
      <v-card-actions>
        <v-btn color="error" @click="restore_init('editPermissionGroupDialog')">取消</v-btn>
        <v-btn color="success" @click="editPermissionGroup()">确定</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>
