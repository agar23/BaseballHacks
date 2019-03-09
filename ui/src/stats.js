import React, { Component } from 'react';
import { ListGroup, ListGroupItem } from 'reactstrap';


class Stats extends Component {
  render() {
    return (
        <ListGroup className='list'>
                  <ListGroupItem><b>Min Range:</b> {this.props.min}</ListGroupItem>
                  <ListGroupItem><b>Max Range:</b> {this.props.max}</ListGroupItem>
                  <ListGroupItem><b>Pearson Correlation: </b> {this.props.pearson}</ListGroupItem>
        </ListGroup>
    );
  }
};

export default Stats;