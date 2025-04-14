<template>
    <div class="movie-form-container">
        <div v-if="errors.length" class="alert alert-danger">
            <ul><li v-for="(error, index) in errors" :key="index">{{ error }}</li></ul>
        </div>
        
        <div v-if="successMessage" class="alert alert-success">
            {{ successMessage }}
        </div>
        
        <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data" >
            <div class="form-group mb-3">
                <label for="title" class="form-label">Title</label>
                <input type="text" name="title" id="title" class="form-control" v-model="movie.title">
            </div>
            
            <div class="form-group mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea name="description" id="description" class="form-control" rows="4" v-model="movie.description"></textarea>
            </div>
            
            <div class="form-group mb-3">
                <label for="poster" class="form-label">Poster</label>
                <input type="file" name="poster" id="poster" class="form-control" @change="handleFileUpload">
                <small class="form-text text-muted">Please upload a JPG or PNG image for the movie poster.</small>
            </div>
            
            <div class="form-group mt-4">
                <button type="submit" class="btn btn-primary">Save Movie</button>
            </div>
        </form>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    
    // Reactive property for CSRF token
    const csrf_token = ref("");
    // Existing data and methods for form handling
    const movie = ref({
        title: "",
        description: "",
    });
    const poster = ref(null);
    const errors = ref([]);
    const successMessage = ref("");
    
    // Method to fetch CSRF token
    function getCsrfToken() {
        fetch("/api/v1/csrf-token")
        .then(response => {
            if (!response.ok) {
            throw new Error("Failed to get CSRF token");
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
        .catch(err => {
            console.error("Error fetching CSRF token", err);
        });
    }
    
    // Fetch CSRF token when component is mounted
    onMounted(() => {
        getCsrfToken();
    });
    
    function handleFileUpload(event) {
        poster.value = event.target.files[0];
    }
    
    function saveMovie() {
        errors.value = [];
        successMessage.value = "";
    
        const movieForm = document.getElementById('movieForm');
        const form_data = new FormData(movieForm);

        form_data.append("title", movie.value.title);
        form_data.append("description", movie.value.description);
        form_data.append("poster", poster.value);
        form_data.append("csrf_token", csrf_token.value); // Add CSRF token to form data
    
        fetch("/api/v1/movies", {
            method: "POST",
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(response => {
            if (!response.ok) {
            throw new Error("Failed to save movie");
            }
            return response.json();
        })
        .then(data => {
                successMessage.value = data.message;
                movie.value = { title: "", description: "" };
                poster.value = null;
        })
        .catch (err => {
        errors.value = ["An error occurred while saving the movie."];
        console.error("Error saving movies: ", err);
        });
    }
</script>

    
    // const title = ref("");
    // const description = ref("");
            

//             function getCsrfToken() {
//             fetch("/api/v1/csrf-token")
//                 .then(res => {
//                 if (!res.ok) {
//                     throw new Error(`Failed to fetch CSRF token: ${res.status}`);
//                 }
//                 return res.json();
//                 })
//                 .then(data => {
//                 console.log("CSRF token received");
//                 csrf_token.value = data.csrf_token;
//                 })
//                 .catch(error => {
//                 console.error("Error fetching CSRF token:", error);
//                 errors.value = ["Failed to fetch CSRF token. Please refresh the page."];
//                 });
//             }

//             onMounted(() => {
//                 getCsrfToken();
//             });

//             return {
//                 title,
//                 description,
//                 poster,
//                 csrf_token,
//                 errors,
//                 successMessage,
//                 handleFileUpload: (event) => {
//                     poster.value = event.target.files[0];
//                 },
//                 saveMovie: () => {
//                     errors.value = [];
//                     successMessage.value = "";

//                     let movieForm = document.getElementById('movieForm');
//                     let form_data = new FormData(movieForm);

//                     form_data.append("csrf_token", csrf_token.value);
//                     form_data.append("title", title.value);
//                     form_data.append("description", description.value);
//                     form_data.append("poster", poster.value);

//                     fetch("/api/v1/movies", {
//                         method: "POST",
//                         body: form_data,
//                         headers: {
//                             "X-CSRFToken": csrf_token.value,
//                         },
//                     })
//                     .then((response) => response.json())
//                     .then((data) => {
//                         if (data.success) {
//                             successMessage.value = "Movie saved successfully!";
//                         } else {
//                             errors.value = [
//                                 { message: data.error || "Failed to save the movie." },
//                             ];
//                         }
//                     })
//                     .catch((error) => {
//                         console.error("Fetch Error:", error);
//                         errors.value = [
//                             { message: "An unexpected error occurred." },
//                         ];
//                     });
//                 },
//             };
//         },
//     };
// 
