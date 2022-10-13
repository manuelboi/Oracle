// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract StudentCurriculum {


    // Structs
    struct Exam {
        int id;
        int mark;
    }

    struct Career {
        int id;
        string studyCourse;
        Exam[] exams;
    }
    
    struct Student {
        string id;
        string name;
        string surname;
        Career[] careers;
    }


    //Events
    event dataRequestEvent(address adr);
    event dataReadyEvent();


    // Attributes
    address _ad;
    Student _student;


    // Constructor
    constructor() {
        _ad = address(0);
    }


    // Functions
    function emitDataRequestEvent() public {
        _ad = msg.sender;
        emit dataRequestEvent(_ad);
    }

    function setData(Student calldata student) public {
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