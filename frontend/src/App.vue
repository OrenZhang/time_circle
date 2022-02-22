<template>
    <el-config-provider :locale="zhCn">
        <el-container v-loading="mainLoading" class="app-container">
            <el-header class="app-header" height="61px">
                <div class="el-menu-demo">
                    <div class="menu">
                        <router-link to="/" class="header-menu-home">
                            <img src="/favicon.webp" alt="logo.jpg" style="width: 32px; height: 32px; margin: 0 10px 0 0;">
                            <h2 class="header-menu-home-title">
                                Time
                            </h2>
                        </router-link>
                        <el-menu :default-active="activeIndex" :router="true" mode="horizontal" :ellipsis="false">
                            <el-menu-item v-for="item in menu" v-show="!item.disabled" :key="item.index" :route="item.route" :index="item.index">
                                {{ item.name }}
                            </el-menu-item>
                        </el-menu>
                    </div>
                </div>
            </el-header>
            <el-main>
                <router-view />
            </el-main>
        </el-container>
    </el-config-provider>
</template>

<script setup>
    import { computed, ref } from 'vue'
    import { useStore } from 'vuex'
    import zhCn from 'element-plus/es/locale/lang/zh-cn'

    // vuex
    const store = useStore()
    const mainLoading = computed(() => store.state.mainLoading)

    // 菜单
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
</script>

<style>
    @import "./assets/App.css";
</style>
