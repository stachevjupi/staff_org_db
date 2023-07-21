const vm = new Vue({ // Again, vm is our Vue instance's name for consistency.
    el: '#vm',
    delimiters: ['[[', ']]'],
    data: {
    checkboxValue: false,
    selectedOption: '',
    selectedOptionChapter: '',
    isVisible: false,
  },
  methods: {
    toggleDiv() {
      // Toggle the checkbox value
      this.checkboxValue = !this.checkboxValue;
    },
    toggleElement() {
      this.isVisible = !this.isVisible;
    },
  }
})
