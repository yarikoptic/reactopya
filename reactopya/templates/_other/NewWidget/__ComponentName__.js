import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
const config = require('./{{ NewWidget.ComponentName }}.json');

export default class {{ NewWidget.ComponentName }} extends Component {
    static title = '{{ NewWidget.description }}'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            status: '',
            status_message: ''
        }
    }
    componentDidMount() {
        this.pythonInterface = new PythonInterface(this, config);
        this.pythonInterface.start();
    }
    componentDidUpdate() {
        this.pythonInterface.update();
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    render() {
        return (
            <React.Fragment>
                <div>{{ NewWidget.ComponentName }}</div>
                <RespectStatus {...this.state}>
                    <div>Render {{ NewWidget.ComponentName }} here</div>
                </RespectStatus>
            </React.Fragment>
        )
    }
}

class RespectStatus extends Component {
    state = {}
    render() {
        switch (this.props.status) {
            case 'running':
                return <div>Running: {this.props.status_message}</div>
            case 'error':
                return <div>Error: {this.props.status_message}</div>
            case 'finished':
                return this.props.children;
            default:
                return <div>Unknown status: {this.props.status}</div>
        }
    }
}