app.component("card", {
    
    template:
    `
    
    `,
    data() {
        return {
            users: [],
            errormsg: ''
        }
    },
    created() {
        var url = "http://localhost/nsbuddy/users";
        axios
        .get(url)
        .then((response)=> {
            console.log(response.data.data)
            if (response.data.code == 200) {
                // orders of all customers
                this.users = response.data.data.users; 

            } else {
                this.errormsg = response.data.message;
            }
        })
        .catch(err => {
            this.errormsg = err.message;
        })
    }
})

