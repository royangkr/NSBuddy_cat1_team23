app.component("cardSection", {

    props: ['type', 'cardlist'],

    emits: ['close'],

    template:
    `
    <div class='cards row  row-cols-1 row-cols-sm-2 row-cols-lg-4 align-items-center' v-if="errormsg.length == 0">
        <div class="p-1 col" v-for='oneCard, idx in this.cardlist.carditems' style="width: 18rem;">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{oneCard[0]}}</h5>
                    <h6 class="card-subtitle mb-2 text-muted" v-if="oneCard.length > 3">{{oneCard[3]}}</h6>
                    
                    <p class="card-text"  :style="[oneCard[1] == 'failed' ? 'color:red' : oneCard[1] == 'ongoing' ? 'color:orange' : '']">{{oneCard[1]}}</p>
                    <a class="btn btn-danger" style='color:white' @click="$emit('close', idx, type)">Close</a>
                </div>
                <div class="card-footer text-muted">
                    {{oneCard[2]}}
                </div>
            </div>
        </div>
    </div>

    <div class='text-danger' v-if="errormsg.length > 0">
        <p class="card-text text-danger">{{errormsg}}</p>
    </div>
    `,

    data() {
        return {
            errormsg: ''
        }
    },

    methods: {
        close() {
            this.$emit("close");
        },
    }
})