import React, { Component } from 'react';
import Chart from './chart';
import './App.css';
import {
  Accordion,
  AccordionItem,
  AccordionItemTitle,
  AccordionItemBody,
} from 'react-accessible-accordion';
import 'react-accessible-accordion/dist/fancy-example.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Jumbotron, Container } from 'reactstrap';
import logo from './resources/redSox.png'

class App extends Component {
  render() {
    return (
      <div className="App">
        <div>
          <Jumbotron fluid className='jumbo'>
            <Container fluid>
              <div className='row'>
                <div className='col-sm topBox'>
                  <h1 className="display-4 mainHeading">Hey, Boston Red Sox</h1>
                  <p className="lead subHeading">Do this to win <span className='subMinHeading'>(it's backed by data science)</span></p>
                </div>
                <div className='col-sm'>
                  <img  src={logo} alt="fireSpot" height="200" width="200"/>
                </div>
              </div>     
            </Container>
          </Jumbotron>
      </div>
        <Accordion>
        <AccordionItem>
            <AccordionItemTitle>
                <h3>Optimal Attendance</h3>
                <div>Optimal attendance range for target wins of >95 per season: 1,556,402 - 3,062,699</div>
            </AccordionItemTitle>
            <AccordionItemBody>
                <Chart 
                width={800}
                height={500}/>
            </AccordionItemBody>
        </AccordionItem>
    </Accordion>
      </div>
    );
  }
}

export default App;
