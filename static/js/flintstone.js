var SearchBox = React.createClass({
  handleSearchSubmit: function(text){
    console.log(text);
    this.setState({ query: text });
  },
  getInitialState: function(){
    return { query: "" }
  },
  render: function() {
    return (
      <div className="searchBox">
        <SearchForm onSearchSubmit={this.handleSearchSubmit} />
        <SearchResults query={this.state.query } />
      </div>
    );
  }
});

var SearchForm = React.createClass({
  handleSubmit: function(e){
    e.preventDefault();
    var text = React.findDOMNode(this.refs.search_text).value.trim();
    if (!text) return;
    this.props.onSearchSubmit(text);
  },
  render: function() {
    return (
      <div className="searchForm">
        <form onSubmit={ this.handleSubmit }>
          <input type="text" ref="search_text" />
        </form>
      </div>
    );
  }
});


var SearchResults = React.createClass({
  getInitialState: function() {
    return { data: [] };
  },
  loadSearchResults: function(props) {
    console.log('hit loadsearch');
    console.log(props);
    if (!props.query) return;
    $.ajax({
      url: "/series/search",
      dataType: 'json',
      data: {
        search_text: props.query
      },
      success: function(data) {
        console.log(data);
        if (data && data.seriess) {
          this.setState({data: data.seriess});
        }
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(props, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.loadSearchResults(this.props);
  },
  componentWillReceiveProps: function (props) {
    this.loadSearchResults(props);
  },
  render: function() {
    var searchItems = this.state.data.map(function(item){
      return (
        <li><span className="title" series-id="{ item.series_id }">{ item.title }</span></li>
      );
    });

    return (
      <div className="searchResults">
        <ul>
          { searchItems }
        </ul>
      </div>
    );
  }
});

React.render(
  <SearchBox />,
  document.getElementById('content')
);
