<script>
export default {
  name: "inputDialog",
  data: () => {
    return {
      flag: false,
      input: null,
      title: "",
      label: "",
      type: "text",
      confirmationCallback: null,
      cancelCallback: null
    }
  }
}
</script>

<template>
  <v-dialog
      id="inputDialog"
      v-model="flag"
      activator="parent"
      min-width="400px"
      width="auto"
      persistent
    >
      <v-card>
        <v-card-title>{{ title }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="input" :label="dialogs.inputDialog.label" :type="dialogs.inputDialog.type"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="cancelCallback ? cancelCallback() : this.dialogs.inputDialog.flag = false">取消</v-btn>
          <v-btn color="success" @click="confirmationCallback(input);flag = false">确定</v-btn>
        </v-card-actions>
      </v-card>
  </v-dialog>
</template>

<style scoped>

</style>
