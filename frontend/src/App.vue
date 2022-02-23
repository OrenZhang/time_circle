<template>
    <t-loading :loading="mainLoading" fullscreen />
    <div v-if="!mainLoading" style="width: 100%; height: 100%">
        <router-view />
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import { useStore } from 'vuex'

    // vuex
    const store = useStore()
    const mainLoading = computed(() => store.state.mainLoading)

    // 菜单
    const activeIndex = ref('home')
    const menu = ref([
        {
            name: 'Home',
            route: {
                name: 'Home'
            },
            index: 'home',
            disabled: false
        }
    ])

    onMounted(() => store.dispatch('getUserInfo'))
</script>

<style>
@import "./assets/App.css";
</style>
