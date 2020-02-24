import React, { Component } from 'react';
import './HotTopic.css'

import HotTopic from './HotTopic';
import MySlider from './Slider';
import DateSelector from './DatePicker';
import ButtonTopic from './ButtonTopic';
import { debounce } from 'throttle-debounce';

class HotTopicWrapper extends React.Component {
    constructor() {
        super()
        this.onChangeSlider = debounce(80, this.handleSlide)
        this.state = {
            data: [{}],
            numTopics: 5,
            startDate: new Date(2020, 0, 1),
            endDate: new Date(2020, 1, 12),
            focusTopic: {},
            topic: '',
        }
    }

    componentDidMount() {
        this.fetchHotTopic()
        this.fetchNewest()
    }

    fetchHotTopic = () => {
        const { numTopics, startDate, endDate } = this.state
        const startDateJSON = startDate.toJSON().split('T')[0]
        const endDateJSON = endDate.toJSON().split('T')[0]
        fetch(`http://127.0.0.1:8000/hot_topic2/${numTopics}/${startDateJSON}/${endDateJSON}`)
            .then(response => response.json())
            .then(data => { this.setState({ data: data }) })
            .then(() => this.handleTopic(Object.keys(this.state.data[0])[0]))

    }

    fetchNewest = () => {
        const { startDate, endDate, topic } = this.state
        const startDateJSON = startDate.toJSON().split('T')[0]
        const endDateJSON = endDate.toJSON().split('T')[0]
        fetch(`http://127.0.0.1:8000/newest/${startDateJSON}/${endDateJSON}/${topic}`)
            .then(response => response.json())
            .then(newest => { this.setState({ focusTopic: newest }) })
    }

    handleSlide = (numTopics) => {
        this.setState({
            numTopics
        }, () => {
            this.fetchHotTopic()
        })
    }

    handleStartDateChange = (date) => {
        this.setState({
            startDate: date,
        }, () => {
            this.fetchHotTopic()
        })
    }

    handleEndDateChange = (date) => {
        this.setState({
            endDate: date,
        }, () => {
            this.fetchHotTopic()
        })
    }

    handleTopic = (topic) => {
        console.log(topic)
        this.setState({
            topic: topic,
        }, () => {
            this.fetchNewest()
        })
    }

    render() {
        return (
            <div className='box-utama'>
                <div className='hot-topic'>
                    <div className='date-selector'>
                        <DateSelector
                            onDateChange={this.handleStartDateChange}
                            selectedDate={this.state.startDate}
                            textTitle={'Date Start'} />
                        <DateSelector
                            selectedDate={this.state.endDate}
                            onDateChange={this.handleEndDateChange}
                            textTitle={'Date End'} />
                    </div>
                    <div className='slider'>
                        <h6 className='m-3'>Number of Topics</h6>
                        <MySlider onSlide={this.onChangeSlider} value={this.state.numTopics} />
                    </div>
                    <HotTopic data={this.state.data} />
                </div>
                <div className='single-topic'>
                    <div className='topic'>
                        <ButtonTopic topic_data={this.state.data} onHandleTopic={this.handleTopic} />
                    </div>
                    <div className='focus-topic'>
                        <h3>{this.state.focusTopic.title}</h3>
                        <p>{this.state.focusTopic.date}</p>
                        <div className='float'>
                            <img src={this.state.focusTopic.media}></img>
                        </div>
                        <p>{this.state.focusTopic.contentRaw}</p>
                    </div>
                </div>
            </div >
        )
    }
}

export default HotTopicWrapper;