<template>
    <div class="h-center v-center h-100">
        <el-empty :description="description">
        </el-empty>
    </div>
</template>


<script setup>
    const props = defineProps({
        description: {
            type: String,
            default: '资源未找到'
        }
    })
</script>

<style scoped>

</style>