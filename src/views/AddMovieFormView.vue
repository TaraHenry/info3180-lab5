<template>
    <div class="container">
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <h1 class="mt-4 mb-4">Add a New Movie</h1>
                <MovieForm />
            </div>
        </div>
    </div>
</template>

<script>
    import MovieForm from '@/components/MovieForm.vue'

    export default {
        name: 'AddMovieFormView',
        components: {
            MovieForm
        }
    }
</script>

<style scoped>
    .container {
        padding-top: 20px;
        padding-bottom: 40px;
    }
</style>