<template>
    <div class="overview-container">
        <t-breadcrumb>
            <t-breadcrumbItem v-for="item in breadItems" :key="item" @click="clickBread(item)">
                {{ item.title }}
            </t-breadcrumbItem>
        </t-breadcrumb>
        <t-date-picker mode="date" range :placeholder="['开始时间', '结束时间']" v-model="dateRange" @change="changeData" />
        <div class="echart-box">
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
    import { overviewChartAPI, overviewCommonAPI } from '../api/overview'
    import { MessagePlugin } from 'tdesign-vue-next'
    import * as echarts from 'echarts/core'
    import { PieChart } from 'echarts/charts'
    import {
        GridComponent,
        DatasetComponent,
        TransformComponent
    } from 'echarts/components'
    import { LabelLayout, UniversalTransition } from 'echarts/features'
    import { SVGRenderer } from 'echarts/renderers'
    echarts.use([
        PieChart,
        GridComponent,
        DatasetComponent,
        TransformComponent,
        LabelLayout,
        UniversalTransition,
        SVGRenderer
    ])

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
            initEcharts(res.data.data)
        },
        err => MessagePlugin.error(err.data.msg)
    )
    onMounted(loadData)

    const initEcharts = (data) => {
        const myChart = echarts.init(document.getElementById('echart-graph-0'))
        myChart.setOption({
            xAxis: {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
            },
            yAxis: {},
            series: [
                {
                    type: 'pie',
                    data: data,
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