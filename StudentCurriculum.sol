// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract StudentCurriculum {


    // Structs
    struct Teaching {
        int id;
        string name;
    }

    struct Exam {
        int id;
        int mark;
        uint date;
        Teaching teaching;
    }

    struct Career {
        string id;
        string studyCourse;
        bool completed;
        Exam[] exams;
    }
    
    struct Student {
        string id;
        string name;
        string surname;
        Career[] careers;
    }

    mapping(address => Student) public students;


    //Events
    event dataRequestEvent(address adr);
    event dataReadyEvent(address adr);


    // Functions
    function emitDataRequestEvent() public {
        emit dataRequestEvent(msg.sender);
    }

    function setData(address adr, Student calldata student) public {
        students[adr] = student;
    }

    function emitDataReadyEvent(address adr) public {
        emit dataReadyEvent(adr);
    }

    function requestData() public view returns(Student memory student) {
        return students[msg.sender];
    }


}