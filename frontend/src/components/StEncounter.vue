<template>
    <div class="st-home-box">
        <div style="font-size: 16px">
            在 {{ data.year }} 年里，记录最多的事项是
        </div>
        <div>
            <span class="total_count">{{ data.item_name }}</span>
        </div>
        <div>
            <div style="font-size: 18px">
                累计 <span class="total_minute">{{ data.item_record_during }}</span> 天的时光里, 记录了 <span class="total_hour">{{ data.item_record_count }}</span> 次
            </div>
        </div>
        <img src="/extra-assets/imgs/st-encounter-bg.png" alt="st-home-bg.png" class="bg-img">
        <div class="arrow-box">
            <i class="fa-solid fa-angle-up" v-show="hasLast" @click="$emit('last')" />
            <i class="fa-solid fa-angle-down" v-show="hasNext" @click="$emit('next')" />
        </div>
    </div>
</template>

<script setup>
    import moment from 'moment'

    defineProps({
        data: {
            type: Object,
            default: {
                'year': '0000',
                'item_name': '',
                'item_record_during': 0,
                'item_record_count': 0
            }
        },
        hasNext: {
            type: Boolean,
            default: false
        },
        hasLast: {
            type: Boolean,
            default: false
        }
    })
    defineEmits(['last', 'next'])

    const transTime = (seconds) => parseInt(moment.duration(seconds, 'seconds').asHours())
    const transTime2Minutes = (seconds) => parseInt(moment.duration(seconds, 'seconds').asMinutes())
</script>

<style scoped>
.st-home-box {
    min-width: 360px;
    width: 100%;
    height: 100%;
    color: white;
    background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    box-sizing: border-box;
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.total_count {
    color: var(--td-brand-color-5);
    font-size: 32px;
    line-height: 60px;
}

.total_hour {
    color: var(--td-brand-color-5);
    font-size: 24px;
    line-height: 40px;
}

.total_minute {
    color: var(--td-brand-color-5);
    font-size: 24px;
    line-height: 40px;
}

.bg-img {
    width: 100%;
    max-width: 360px;
}

.arrow-box {
    display: flex;
}

.arrow-box i {
    font-size: 24px;
}

.arrow-box i:nth-of-type(2) {
    margin-left: 36px;
}
</style>