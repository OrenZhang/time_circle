<template>
    <div class="detail-container">
        <t-breadcrumb>
            <t-breadcrumbItem v-for="item in breadItems" :key="item" @click="clickBread(item)">
                {{ item.title }}
            </t-breadcrumbItem>
        </t-breadcrumb>
        <div class="detail-header">
            <t-date-picker mode="date" :disable-date="disableDate" range :placeholder="['开始时间', '结束时间']" v-model="dateRange" @change="changeData" />
            <t-pagination
                v-model="paginator.page"
                v-model:pageSize="paginator.size"
                :total="paginator.count"
                :page-size-options="[10, 20, 50, 100]"
                @page-size-change="onPageSizeChange"
                @current-change="onCurrentChange"
            />
        </div>
        <div class="detail-main">
            <t-table
                row-key="index"
                :data="items"
                :columns="columns"
                :stripe="false"
                :bordered="false"
                :hover="false"
                :table-layout="'auto'"
                :size="'medium'"
            >
                <template #name="{ row }">
                    <div>{{ row.full_name }}</div>
                    <div v-if="row.desc" style="color: var(--td-text-color-placeholder)">
                        {{ row.desc }}
                    </div>
                </template>
            </t-table>
        </div>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue'
    import moment from 'moment'
    import { MessagePlugin } from 'tdesign-vue-next'
    import { loadItemsAPI } from '../api/circle'
    import { useRouter } from 'vue-router'

    const loading = ref(false)
    const setLoading = (status) => {
        if (status) {
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
            }, 600)
        }
    }

    const router = useRouter()
    const breadItems = ref([
        {
            path: { name: 'Home' },
            title: 'Home'
        },
        {
            path: 0,
            title: 'Item'
        }
    ])
    const clickBread = (item) => {
        if (typeof item.path === 'object') {
            router.push(item.path)
        }
    }

    const dateRange = ref([new moment().format('YYYY-MM-DD'), new moment().format('YYYY-MM-DD')])
    const changeData = (value) => {
        dateRange.value = value
        loadData()
    }
    const disableDate = (date) => date > new Date()

    const paginator = ref({
        page: 1,
        size: 10,
        count: 0
    })
    const onCurrentChange = (page) => {
        paginator.value.page = page
        loadData()
    }
    const onPageSizeChange = (size) => {
        paginator.value.page = 1
        paginator.value.size = size
        loadData()
    }

    const items = ref([])
    const loadData = () => {
        const startAt = dateRange.value[0]
        const endAt = dateRange.value[1]
        loadItemsAPI(paginator.value.page, paginator.value.size, startAt, endAt).then(
            res => {
                items.value = res.data.data.results
                paginator.value.count = res.data.data.count
            },
            err => MessagePlugin.error(err.data.msg)
        )
    }
    onMounted(loadData)

    const columns = ref([
        {
            colKey: 'id',
            title: 'ID',
            width: 100
        },
        {
            colKey: 'name',
            title: '类别'
        },
        {
            colKey: 'start_at',
            title: '开始时间',
        },
        {
            colKey: 'end_at',
            title: '结束时间',
        },
        {
            colKey: 'duration_format',
            title: '时长(s)',
        },
    ])
</script>

<style scoped>
.detail-container {
    height: 100%;
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
}

.detail-header {
    display: flex;
    padding-bottom: 20px;
}

.t-breadcrumb {
    padding-bottom: 20px;
}

.detail-header .t-date-picker {
    width: 100%;
    margin-right: 20px;
}

.detail-header :deep(.t-pagination__total) {
    margin-right: 20px;
}

@media screen and (max-width: 600px) {
    .detail-header {
        flex-direction: column;
    }
    .detail-header .t-date-picker {
        margin-bottom: 20px;
        margin-right: 0;
    }
}
</style>