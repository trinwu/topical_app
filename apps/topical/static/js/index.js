let app = Vue.createApp({
    data() {
        return {
            posts: [],
            newPostText: "",
            tags: [],
            activeTags: new Set(),
            user_email: null,
        };
    },
    computed: {
        filteredPosts() {
            if (this.activeTags.size === 0) {
                return this.posts;
            }
            return this.posts.filter(post => {
                const postTags = new Set(post.tags.map(t => t.replace('#', '')));
                return [...this.activeTags].some(tag => postTags.has(tag));
            });
        }
    },
    methods: {
        async getPosts() {
            const response = await axios.get('../get_posts');
            this.posts = response.data.posts;
            this.user_email = response.data.user_email;
        },
        async createPost() {
            if (!this.newPostText.trim()) return;
            await axios.post('../create_post', {
                content: this.newPostText
            });
            this.newPostText = "";
            await this.getPosts();
            await this.getTags();
        },
        async deletePost(post_id) {
            await axios.post('../delete_post', {
                post_id: post_id
            });
            await this.getPosts();
            await this.getTags();
        },
        async getTags() {
            const response = await axios.get('../get_tags');
            this.tags = response.data.tags;
        },
        toggleTag(tag) {
            if (this.activeTags.has(tag)) {
                this.activeTags.delete(tag);
            } else {
                this.activeTags.add(tag);
            }
        },
        isTagActive(tag) {
            return this.activeTags.has(tag);
        }
    },
    mounted() {
        this.getPosts();
        this.getTags();
    }
});

app.mount("#app");
