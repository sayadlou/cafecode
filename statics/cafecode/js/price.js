let calcApp = new Vue({
  delimiters: ['[[', ']]'],
  el: '#shop-items',
  data:{
    selectedItems: [],
    itemList: [
        {
            name: 'Paypal Payment',
            icon: '1.png',
            value: 111,
            isChecked: false,
        },
        {
          name: 'Filter Produkts',
          icon: '1.png',
          value: 111,
          isChecked: false,
        },
        {
          name: 'Dynamic Search',
          icon: '1.png',
          value: 111,
          isChecked: false,
        },

    ],
  },

  created(){
       
  },

computed:{
  
  },

methods:{
    calc(item){
      if(item.isChecked)
          this.item.isChecked = false;
          return;
      },
  },
 
  
});
