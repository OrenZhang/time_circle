<template>
    <t-layout class="admin-container">
        <t-header>
            <t-breadcrumb>
                <t-breadcrumbItem v-for="item in breadItems" :key="item" @click="clickBread(item)">
                    {{ item.title }}
                </t-breadcrumbItem>
            </t-breadcrumb>
        </t-header>
        <t-content>
            <t-row :gutter="20">
                <t-col v-for="(item, index) in categories" :key="item" :span="span" class="category-item-col">
                    <Category :data="item" :index="index" @click="nextLevel(item)" />
                </t-col>
            </t-row>
        </t-content>
        <t-footer v-show="currentParentId !== 0">
            <t-row :gutter="20">
                <t-col :span="span" class="category-item-col">
                    <Category :data="{ name: '删除' }" @click="deleteVisible = true" />
                </t-col>
            </t-row>
        </t-footer>
        <t-dialog
            v-model:visible="visible" :cancel-btn="null" :confirm-btn="null"
            header="创建目录" class="create-dialog">
            <t-form :data="formData" label-width="60px" :colon="true" @submit="onSubmit">
                <t-form-item label="名称" name="name" :rules="rules">
                    <t-input v-model="formData.name" placeholder="请输入内容" />
                </t-form-item>
                <t-form-item style="padding-top: 8px" class="submit-button">
                    <t-button theme="primary" type="submit" style="margin-right: 10px">
                        提交
                    </t-button>
                </t-form-item>
            </t-form>
        </t-dialog>
        <t-dialog
            v-model:visible="deleteVisible"
            header="删除确认"
            body="确认删除当前目录及所有子目录吗？"
            :on-confirm="deleteCategory"
        />
    </t-layout>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import { createCategoryAPI, deleteCategoryAPI, getCurrentCategoryAPI, loadLevelDataAPI } from '../api/circle'
    import { MessagePlugin } from 'tdesign-vue-next'
    import Category from '../components/Category.vue'
    import { useRouter } from 'vue-router'

    const visible = ref(false)
    const formData = ref({
        name: '',
        parent_id: 0
    })
    const rules = ref([
        { required: true, message: '必填', type: 'error' }
    ])
    const onSubmit = (context) => {
        if (context.validateResult !== true) {
            return
        }
        visible.value = false
        createCategoryAPI(formData.value).then(
            res => loadLevelData(),
            err => MessagePlugin.error(err.data.msg)
        )
    }

    const router = useRouter()

    const width = ref(window.innerWidth)
    const span = computed(() => {
        if (width.value >= 1200) {
            return 2
        } else if (width.value >= 800) {
            return 3
        } else if (width.value > 400) {
            return 4
        } else {
            return 12
        }
    })
    window.onresize = () => {width.value = window.innerWidth}

    const breadItems = ref([
        {
            path: { name: 'Home' },
            title: 'Home'
        },
        {
            path: 0,
            title: 'Category'
        }
    ])

    const currentParentId = ref(0)
    const currentCategory = ref({})
    const categories = ref([])
    const loadLevelData = () => loadLevelDataAPI(currentParentId.value).then(
        res => {
            categories.value = res.data.data
            categories.value.push({ name: '+', id: '+' })
        },
        err => MessagePlugin.error(err.data.msg)
    )
    const getCurrentCategory = () => {
        if (currentParentId.value === 0) {
            return
        }
        getCurrentCategoryAPI(currentParentId.value).then(
            res => currentCategory.value = res.data.data,
            err => MessagePlugin.error(err.data.msg)
        )
    }
    onMounted(loadLevelData)
    onMounted(getCurrentCategory)

    const clickBread = (item) => {
        if (typeof item.path === 'object') {
            router.push(item.path)
        } else {
            if (item.path === currentParentId.value) {
                loadLevelData()
            } else {
                jumpBread(item.path)
                nextLevel({ id: item.path, name: item.title })
            }
        }
    }

    const jumpBread = (path) => {
        let index
        for (const i in breadItems.value) {
            if (breadItems.value[i].path === path) {
                index = i
            }
        }
        breadItems.value = breadItems.value.slice(0, index)
    }

    const nextLevel = (item) => {
        if (item.id === '+') {
            visible.value = true
            formData.value = {
                name: '',
                parent_id: currentParentId.value
            }
            return
        }
        currentParentId.value = item.id
        breadItems.value.push({ path: item.id, title: item.name })
        loadLevelData()
        getCurrentCategory()
    }

    const deleteVisible = ref(false)
    const deleteCategory = () => {
        deleteVisible.value = false
        deleteCategoryAPI(currentParentId.value).then(
            res => {
                const lastNode = breadItems.value[breadItems.value.length - 2]
                clickBread(lastNode)
            },
            err => MessagePlugin.error(err.data.msg)
        )
    }
</script>

<style scoped>
.admin-container {
    height: 100%;
    padding: 20px;
}

.admin-container :deep(.t-layout__content) {
    height: 100%;
    overflow: hidden;
    overflow-y: auto;
}

.admin-container :deep(.t-layout__header) {
    height: unset;
}

.admin-container :deep(.t-layout__footer) {
    padding: 20px 0 0 0;
}

.admin-container :deep(.t-layout__footer) .category-item {
    height: 32px;
    margin-bottom: 0;
    background: var(--td-gray-color-5) !important
}

.admin-container :deep(.t-layout__footer) .t-row {
    justify-content: flex-end;
}

.t-breadcrumb {
    padding-bottom: 20px;
}

.submit-button :deep(.t-form__controls-content) {
    float: right;
}

.submit-button :deep(.t-form__controls-content) .t-button {
    margin-right: 0!important;
}

.create-dialog :deep(.t-dialog__body) {
    padding-bottom: 0 !important;
}
</style>