import React from 'react';
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

class DateSelector extends React.Component {
    render() {
        return (
            <React.Fragment>
                <h5 className='m-auto'>{this.props.textTitle}</h5>
                <DatePicker
                    className='form-control'
                    selected={this.props.selectedDate}
                    onChange={e => this.props.onDateChange(e)}
                />
            </React.Fragment>
        );
    }
}

export default DateSelector;