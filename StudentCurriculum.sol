// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract StudentCurriculum {

    // Structs
    struct StudyCourse {
        int id;
        string name;
    }

    struct Course {
        int id;
        string name;
        mapping(uint => StudyCourse) studyCourses;
    }

    struct Exam {
        int id;
        int mark;
        Course course;
    }

    struct Career {
        int id;
        Exam[] exams;
        StudyCourse studyCourse;
    }
    
    struct Student {
        string id;
        string name;
        string surname;
        mapping(uint => Career) careers;
    }

    //Events
    event dataRequestEvent(address adr);
    event dataReadyEvent();

    // Attributes
    address _ad;
    Student _student;

    constructor() {
        _ad = address(0);
    }

    function emitDataRequestEvent() public {
        emit dataRequestEvent(msg.sender);
    }

    function setData(Student memory student) public {
        _student = student;
    }

    function emitDataReadyEvent() public {
        emit dataReadyEvent();
    }

    function requestData() public view returns(Student memory student) {
        if (msg.sender == _ad)
            return _student;
    }

}