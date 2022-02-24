<template>
    <div class="overview-container">
        <t-breadcrumb>
            <t-breadcrumbItem v-for="item in breadItems" :key="item" @click="clickBread(item)">
                {{ item.title }}
            </t-breadcrumbItem>
        </t-breadcrumb>
        <t-date-picker mode="date" range :placeholder="['开始时间', '结束时间']" v-model="dateRange" @change="changeData" />
        <div class="echart-box" v-show="showEchart">
            <div id="echart-graph-0" style="width: 100%; height:360px;" />
        </div>
        <t-table
            row-key="index"
            :data="categories"
            :columns="columns"
            :stripe="false"
            :bordered="false"
            :hover="true"
        />
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import moment from 'moment'
    import { overviewCommonAPI } from '../api/overview'
    import { MessagePlugin } from 'tdesign-vue-next'
    import * as echarts from 'echarts'

    const router = useRouter()

    const breadItems = ref([
        {
            path: { name: 'Home' },
            title: 'Home'
        },
        {
            path: 0,
            title: 'Overview'
        }
    ])

    const clickBread = (item) => {
        if (typeof item.path === 'object') {
            router.push(item.path)
        }
    }

    const categories = ref([])
    const columns = ref([
        {
            align: 'left',
            colKey: 'full_name',
            title: '目录',
        },
        {
            align: 'left',
            colKey: 'duration_format',
            width: 120,
            title: '时长',
        }
    ])

    const dateRange = ref([new moment().format('YYYY-MM-DD'), new moment().format('YYYY-MM-DD')])
    const changeData = (value) => {
        dateRange.value = value
        loadData()
    }

    const loadData = () => overviewCommonAPI({
        start_date: dateRange.value[0],
        end_date: dateRange.value[1]
    }).then(
        res => {
            categories.value = res.data.data
            if (categories.value.length === 0) {
                showEchart.value = false
            } else {
                initEcharts(categories.value)
            }
        },
        err => MessagePlugin.error(err.data.msg)
    )
    onMounted(loadData)

    const showEchart = ref(true)
    const initEcharts = (data) => {
        const source = []
        const fields = []
        for (const category of data) {
            source.push({
                name: category.full_name,
                value: category.duration
            })
            fields.push(category.full_name)
        }
        const myChart = echarts.init(document.getElementById('echart-graph-0'))
        myChart.setOption({
            xAxis: {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                data: fields
            },
            yAxis: {},
            series: [
                {
                    type: 'pie',
                    data: source,
                    color: [
                        '#48c79c',
                        '#f78d94',
                        '#699ef5',
                    ],
                    roseType: 'area'
                }
            ],
            grid: { x: 0, y: 0, x2: 0, y2: 0 }
        })
    }
</script>

<style scoped>
.overview-container {
    padding: 20px;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
}

.t-breadcrumb,
.t-date-picker {
    padding-bottom: 20px;
}

.echart-box {
    display: flex;
    margin-top: 20px;
}
</style>