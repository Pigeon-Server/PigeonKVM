<script>
import Audit_table from "@/components/AuditPage/audit_table.vue";
import SystemLog_table from "@/components/AuditPage/systemLog_table.vue";
import AccessLog_table from "@/components/AuditPage/accessLog_table.vue";
import FileChangeLog_table from "@/components/AuditPage/fileChangeLog_table.vue";

export default {
  name: "audit",
  components: {FileChangeLog_table, AccessLog_table, SystemLog_table, Audit_table},
  data: ()=>{
    return {
      tab: null
    }
  }
}
</script>

<template>
  <v-card>
    <v-tabs
      v-model="tab"
    >
      <v-tab value="audit">审计</v-tab>
      <v-tab value="System_log">系统日志</v-tab>
      <v-tab value="Access_log">访问日志</v-tab>
      <v-tab value="File_change_log">文件修改日志</v-tab>
    </v-tabs>
    <v-card-text>
      <v-window v-model="tab">
        <v-window-item value="audit">
          <audit_table></audit_table>
        </v-window-item>
        <v-window-item value="System_log">
          <system-log_table></system-log_table>
        </v-window-item>
        <v-window-item value="Access_log">
          <access-log_table></access-log_table>
        </v-window-item>
        <v-window-item value="File_change_log">
          <file-change-log_table></file-change-log_table>
        </v-window-item>
      </v-window>
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>
