<template>
    <div class="home-container">
        <CircleItem
            v-for="item in menu" :key="item"
            :title="item.title" :bg="item.bg" @click="$router.push(item.path)" />
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import CircleItem from '../components/CircleItem.vue'

    const menu = ref([
        {
            title: 'Time',
            bg: 'var(--td-brand-color-5)',
            path: {
                name: 'Time'
            }
        },
        {
            title: 'Overview',
            bg: 'var(--td-success-color-4)',
            path: {
                name: 'Overview'
            }
        },
        {
            title: 'Item',
            bg: 'var(--td-warning-color-4)',
            path: {
                name: 'Item'
            }
        },
        {
            title: 'Category',
            bg: 'var(--td-error-color-5)',
            path: {
                name: 'Admin'
            }
        }
    ])
</script>

<style scoped>
.home-container {
    width: 100%;
    height: 100%;
    padding: 20px 20%;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}

@media screen and (max-width: 1600px) {
    .home-container {
        padding: 20px 10%;
    }
}

@media screen and (max-width: 600px) {
    .home-container {
        flex-direction: column;
        padding: 10% 20px;
    }
}
</style>
