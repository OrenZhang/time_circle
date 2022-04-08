<template>
    <div class="json-tree-box">
        <t-row>
            <t-col :span="6">
                <div style="padding: 40px; box-sizing: border-box">
                    <t-textarea style="height: calc(100vh - 80px);" v-model="data" />
                </div>
            </t-col>
            <t-col :span="6">
                <div style="padding: 40px; box-sizing: border-box" class="json-tree-div">
                    <json-tree style="overflow: auto; height: 100%" :raw="data" />
                </div>
            </t-col>
        </t-row>
    </div>
</template>

<script setup>
    import JsonTree from 'vue-json-tree'
    import { ref } from 'vue'
    const data = ref('')
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

.json-tree-div {
    background-color: #f7f8f9;
    height: 100%;
}

.json-tree :deep(.json-tree-value-number) {
    color: var(--td-brand-color);
}

.json-tree :deep(.json-tree-value-string) {
    color: var(--td-success-color);
}

@media (prefers-color-scheme: dark) {
    .json-tree-div {
        background-color: unset;
    }

    .json-tree {
        background: unset;
        color: white!important;
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