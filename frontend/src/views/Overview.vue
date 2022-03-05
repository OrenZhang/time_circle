<template>
    <div class="overview-container">
        <t-breadcrumb>
            <t-breadcrumbItem v-for="item in breadItems" :key="item" @click="clickBread(item)">
                {{ item.title }}
            </t-breadcrumbItem>
        </t-breadcrumb>
        <div class="header-box">
            <t-radio-group :value="tabValue" @change="changeTab">
                <t-radio-button value="detail">
                    细化
                </t-radio-button>
                <t-radio-button value="overview">
                    总览
                </t-radio-button>
                <t-radio-button value="rollback" :disabled="true">
                    回溯
                </t-radio-button>
            </t-radio-group>
            <t-date-picker mode="date" :disable-date="disableDate" range :placeholder="['开始时间', '结束时间']" v-model="dateRange" @change="changeData" />
        </div>
        <div class="echart-box">
            <div id="echart-graph-0" v-if="showChart" style="width: 100%; height:360px;" />
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
    import { onMounted, onUnmounted, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import moment from 'moment'
    import { overviewChartAPI, overviewCommonAPI, overviewDetailAPI } from '../api/overview'
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
            title: '类别',
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

    const loadData = () => {
        let promise
        const data = {
            start_date: dateRange.value[0],
            end_date: dateRange.value[1]
        }
        if (tabValue.value === 'overview') {
            promise = overviewCommonAPI(data)
        } else if (tabValue.value === 'detail') {
            promise = overviewDetailAPI(data)
        }
        promise.then(
            res => {
                categories.value = res.data.data
                initEcharts(res.data.data)
            },
            err => MessagePlugin.error(err.data.msg)
        )
    }

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

    const disableDate = (date) => date > new Date()

    const showChart = ref(true)
    onMounted(() => showChart.value = true)
    onUnmounted(() => showChart.value = false)

    const tabValue = ref('detail')
    const changeTab = (tab) => {
        tabValue.value = tab
        localStorage.setItem('overviewTabValue', tab)
        loadData()
    }
    onMounted(() => {
        const tab = localStorage.getItem('overviewTabValue')
        if (tab) {
            tabValue.value = tab
        }
        loadData()
    })
</script>

<style scoped>
.overview-container {
    padding: 20px;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
}

.header-box {
    display: flex;
    width: 100%;
}

.header-box .t-date-picker {
    width: 100%;
    margin-left: 20px;
}

@media screen and (max-width: 600px) {
    .header-box {
        flex-direction: column;
    }
    .header-box .t-date-picker {
        margin-top: 20px;
        margin-left: 0;
    }
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