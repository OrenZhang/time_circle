<template>
    <div class="json-tree-box">
        <t-row>
            <t-col :span="6">
                <div style="padding: 40px; box-sizing: border-box">
                    <t-textarea style="height: calc(100vh - 80px);" v-model="data" />
                </div>
            </t-col>
            <t-col :span="6" v-if="!inTime">
                <div style="padding: 40px; box-sizing: border-box" class="json-tree-div">
                    <json-tree style="overflow: auto; height: 100%" :raw="raw" />
                </div>
            </t-col>
            <t-col :span="6" v-else>
                <div style="padding: 40px; box-sizing: border-box" class="json-tree-div">
                    <json-tree style="overflow: auto; height: 100%" :raw="data" />
                </div>
            </t-col>
        </t-row>
        <div class="trans-button-box">
            <t-button class="btn-0" @click="inTime = !inTime" :theme="inTime ? 'primary' : 'default'">
                <i class="fa-solid fa-arrows-rotate" />
            </t-button>
            <t-button class="btn-1" @click="raw = data">
                <i class="fa-solid fa-angle-right" />
            </t-button>
            <t-button class="btn-2" @click="raw = initData; data = initData">
                <i class="fa-solid fa-x" />
            </t-button>
        </div>
    </div>
</template>

<script setup>
    import JsonTree from 'vue-json-tree'
    import { ref } from 'vue'

    const initData = '{"1st button": "auto format", "2nd button": "format json", "3rd button": "clear data"}'
    const data = ref('{"1st button": "auto format", "2nd button": "format json", "3rd button": "clear data"}')
    const raw = ref(initData)
    const inTime = ref(true)
</script>

<style scoped>
.json-tree-box {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}

.t-row {
    box-shadow: var(--td-shadow-1);
    border-radius: 5px;
    overflow: hidden;
}

.t-row,
.t-col {
    height: 100%;
}

.json-tree-box :deep(textarea) {
    border: none!important;
    font-size: 12px;
    font-family: Menlo, Monaco, Consolas, monospace;
    color: var(--td-text-color-primary);
}

.json-tree-box :deep(.t-textarea__inner:focus) {
    box-shadow: none!important;
}

.json-tree-box :deep(.json-tree-root) {
    margin: 0;
}

.json-tree-box :deep(textarea)::-webkit-scrollbar-thumb,
.json-tree::-webkit-scrollbar-thumb {
    background: var(--td-brand-color-5);
    border-radius: 0;
}

.json-tree-box :deep(textarea)::-webkit-scrollbar,
.json-tree::-webkit-scrollbar {
    width: 6px;
    background: var(--td-gray-color-1);
    border-radius: 0;
}

.json-tree {
    background-color: unset;
}

.json-tree-div {
    background-color: var(--td-gray-color-1);
    height: 100%;
}

.json-tree :deep(.json-tree-value-number) {
    color: var(--td-brand-color);
}

.json-tree :deep(.json-tree-value-string) {
    color: var(--td-success-color);
}

.trans-button-box .btn-0,
.trans-button-box .btn-1,
.trans-button-box .btn-2 {
    position: fixed;
    z-index: 100;
    display: flex;
    left: 50%;
    top: 50%;
    height: 36px;
    width: 36px;
    border-radius: 0;
    border: unset;
}

.trans-button-box :deep(.t-button--theme-primary) {
    background-color: var(--td-brand-color-5);
}

.trans-button-box .btn-0 {
    margin-left: -18px!important;
    margin-top: -68px!important;
}

.trans-button-box .btn-1 {
    margin-left: -18px!important;
    margin-top: -18px;
    background-color: var(--td-brand-color-5);
}

.trans-button-box .btn-2 {
    margin-left: -18px!important;
    margin-top: 32px!important;
    background-color: var(--td-error-color-5);
}

@media (prefers-color-scheme: dark) {
    .json-tree-div {
        background-color: var(--td-gray-color-12);
    }

    .json-tree :deep(.json-tree-deep),
    .json-tree :deep(.json-tree-row) {
        color: var(--td-gray-color-2);
    }

    .json-tree-box :deep(textarea)::-webkit-scrollbar-thumb,
    .json-tree::-webkit-scrollbar-thumb {
        background: var(--td-brand-color-8);
    }

    .json-tree-box :deep(textarea)::-webkit-scrollbar,
    .json-tree::-webkit-scrollbar {
        background: var(--td-gray-color-6);
    }
}
</style>