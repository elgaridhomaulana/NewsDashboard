import React, { Component } from 'react';

class ButtonTopic extends Component {
	render() {
		const { topic_data, onHandleTopic } = this.props
		const array_length = Object.keys(topic_data[0]).length - 1
		const topics = Object.keys(topic_data[0]).splice(0, array_length)
		return (
			<React.Fragment>
				{
					topics.map((topic, i) => {
						return (
							<button
								key={i}
								type='button'
								className="btn btn-outline-primary m-2"
								onClick={(e) => onHandleTopic(e.target.value)}
								value={topic}
							>
								{topic}
							</button>
						)
					})
				}
			</React.Fragment>

		);
	}
}

export default ButtonTopic;