<template>
    <div class="movies-container">
        <h1>Movies</h1>
    
        <div v-if="loading" class="loading">
            <p>Loading movies...</p>
        </div>
    
        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
        </div>
    
        <div v-else-if="movies.length === 0" class="no-movies">
            <p>No movies available. <router-link to="/movies/create">Add some movies</router-link>!</p>
        </div>
    
        <div v-else class="movies-grid">
            <div v-for="movie in movies" :key="movie.id" class="movie-card">
            <div class="card">
                <img v-if="movie.poster" :src="movie.poster" class="card-img-top" :alt="movie.title">
                <div v-else class="card-img-placeholder">No image available</div>
                
                <div class="card-body">
                <h5 class="card-title">{{ movie.title }}</h5>
                <p class="card-text">{{ movie.description }}</p>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";

    // Reactive state
    const movies = ref([]);
    const loading = ref(true);
    const error = ref(null);

    // Fetch all movies from API
    function fetchMovies() {
        loading.value = true;
        error.value = null;
        
        fetch("/api/v1/movies")
        .then(response => {
            if (!response.ok) {
            throw new Error("Failed to fetch movies");
            }
            return response.json();
        })
        .then(data => {
            movies.value = data.movies;
            loading.value = false;
        })
        .catch(err => {
            console.error("Error fetching movies:", err);
            error.value = "Failed to load movies. Please try again later.";
            loading.value = false;
        });
    }
    
    // Fetch movies when component mounts
    onMounted(() => {
        fetchMovies();
    });
</script>
    
<style scoped>
    .movies-container {
        padding: 20px;
    }
    
    .loading, .error, .no-movies {
        text-align: center;
        margin: 40px 0;
    }
    
    .error {
        color: #dc3545;
    }
    
    .movies-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    
    .movie-card {
        height: 100%;
    }
    
    .card {
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .card-img-top {
        height: 300px;
        object-fit: cover;
    }
    
    .card-img-placeholder {
        height: 300px;
        background-color: #f8f9fa;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6c757d;
    }
    
    .card-title {
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .card-text {
        color: #6c757d;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>