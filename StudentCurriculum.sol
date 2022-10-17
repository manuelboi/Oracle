// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract StudentCurriculum {


    // Structs
    struct Exam {
        int mark;
        uint date;
        string teaching;
    }

    struct Career {
        string id;
        string studyCourse;
        int completed;
    }
    
    struct Student {
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

    function setData(Student calldata student, address adr) public {
        students[adr] = student;
    }

    function emitDataReadyEvent(address adr) public {
        emit dataReadyEvent(adr);
    }

    function requestData(address adr) public view returns(Student memory student) {
        return students[adr];
    }


}