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

var SearchResultItem = React.createClass({
  handleClick: function(e){
    console.log(e);
    console.log(this.props);
    console.log(this.props.item.id);
    this.props.onSelect(this.props.item.id);
  },
  render: function() {
    return (
      <li onClick={this.handleClick}>
        <span className="title"  series-id={ this.props.item.id }>
          { this.props.item.title }
        </span>
      </li>
    );
  }
});

var SearchResults = React.createClass({
  getInitialState: function() {
    return { data: [], show: false };
  },
  loadSearchResults: function(props) {
    if (!props.query) {
      this.setState({ data: [], show: ""});
      return;
    }

    $.ajax({
      url: "/series/search",
      dataType: 'json',
      data: {
        search_text: props.query
      },
      success: function(data) {
        console.log(data);
        if (data && data.seriess) {
          this.setState({data: data.seriess, show: "show"});
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
  selectItem: function(id){
    this.setState({ show: "" });
  },
  render: function() {
    var self = this;
    var classString = "searchResults " + this.state.show;
    return (
      <div className={ classString }>
        <ul>
          { this.state.data.map(function(item){
              return <SearchResultItem key={item.id} item={item} onSelect={ self.selectItem } />;
          })}
        </ul>
      </div>
    );
  }
});

React.render(
  <SearchBox />,
  document.getElementById('content')
);
