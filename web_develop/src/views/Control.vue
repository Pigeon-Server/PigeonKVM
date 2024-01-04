<template>
<!--  <LayoutsHeader/>-->
  <div class="control">
    <DisplaySpace/>
    <StatusBar/>
  </div>
</template>

<script>

</script>

<script setup>
  import LayoutsHeader from "@/layouts/default/Header.vue"
  import DisplaySpace from "@/layouts/ControlsPage/DisplaySpace";
  import StatusBar from "@/layouts/ControlsPage/StatusBar";
  import("@/styles/ControlPage/Control.scss")
</script>
