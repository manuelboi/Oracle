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
        Exam[] exams;
    }
    
    struct Student {
        string name;
        string surname;
        Career[] careers;
    }


    // Attributes
    mapping(address => Student) _students;
    address _oracleAddress = 0x2f2a3bE0f87D2EC706576b457b527eBF1E38d168;


    // Events
    event dataRequestEvent(address adr);
    event dataReadyEvent(address adr);


    //Modifiers
    modifier onlyOracle() {
        require(msg.sender == _oracleAddress, "Only the Oracle can set data.");
        _;
    }


    // Functions
    function emitDataRequestEvent() public {
        emit dataRequestEvent(msg.sender);
    }

    function setData(Student calldata student, address adr) public onlyOracle {
        _students[adr] = student;
    }

    function emitDataReadyEvent(address adr) public {
        emit dataReadyEvent(adr);
    }

    function requestData() public returns(Student memory student) {
        address adr = msg.sender;
        student = _students[adr];
        delete _students[adr];
        return student;
    }


}