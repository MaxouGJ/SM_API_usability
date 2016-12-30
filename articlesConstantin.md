#API Usability - Articles resumes
December 2016 - Montreal<br/>
Quotes and notes from several articles about "API Usability".<br/>
Theses articles are originaly issued from a systematic mapping.


#Article: Some structural measures of API usability
Article about general purpose metrics to measure API usability. List several API method defects.
###Description
- What makes designing a good API particularly onerous is the fact that, unlike the methods internal to a module, an API once deﬁned cannot be changed easily without causing problems for those whose code depends on the API.
- Presents a set of formulas that examine the API method declarations from the perspective of several commonly held beliefs regarding what makes APIs difﬁcult to use.

###Beliefs about defects in API method declarations
- Methods with similar names returning different types of values
```
void add(int ix, Object attrVal);
boolean add(Object attrVal);
```
- Methods with parameter lists containing runs of the same type
``` 
void setShippingAddress(String firstName, String lastName, String street);
```
- Methods with long parameter lists that are dificult to remember
```
static JournalArticle addArticle(
    long userId, long groupId, String articleId,
    boolean autoArticleId, double version, String title,
    String description, String content, String type
);
```
- Methods with similar looking parameters, but with inconsistent sequencing of the parameter names
```
writeStartElement(var namespaceURI, var localName); //namespaceURI then localName
writeEmptyElement(var localName, var namespaceURI); //Same parameters in revers order
```
- Existence of too many methods with nearly identical method names
```
void wait();
void wait3();
void wait4();
```
- Not grouping conceptually similar API methods together
```
.
getAllInputsByName(); //Will be at the top layer of the documentation
.
.
getInputByName(); //Grouped together
getInputByValue();
getInputsByvalue();
.
.
```
- With regard to the concurrency-related behavior of an API, not indicating when a method is thread-safe
- Using exception throwing classes that are too general with respect to the error conditions that result in exceptions
- The poor quality of the API documentation 



#Article: The Factory Pattern in API Design: A Usability Evaluation
Study and comparison between Factory Pattern and class constructor.
###The Factory Pattern
#####Abstract factory 
"Abstract factory" pattern provides an interface with which a client can obtain instances of classes conforming to a particular interface or protocol without having to know precisely what class they are obtaining. 
This has advantages for encapsulation and code reuse, since implementations can be modified without necessitating any changes to client code.
```
AbstractFactory f = AbstractFactory.getDefault();
Widget w = f.createWidget();
```
#####Method factory
The factory method pattern allows a client to obtain objects of an unknown class that implement a particular interface. 
Rather than relying on a separate factory class to create instances of the product classes, the product class itself has a factory method that returns an object that conforms to the interface defined by that class.
```
Widget w = Widget.create();
```
###Why Use a Factory Pattern?
In terms of benefits, the factory pattern enforces the dependency inversion principle: the dependencies of the client are solely to abstract classes and interfaces, and never to the concrete subclasses they are passed.
Second, it decouples the concrete factory and product instances from everything but their point of instantiation.
This means, in the case of the abstract factory, that factories can be swapped in and out simply by changing which factory is instantiated, and without touching any other code.
To avoid requiring the client to directly instantiate a concrete factory subclass, the abstract factory must itself employ the factory method pattern to return a polymorphically typed instance of one of its concrete subclasses.
###Conclusion
Our study finds that the factory pattern erodes the usability of APIs in which it is used. There are alternatives with better usability, such as class clusters, which can be used in many situations in which a factory might normally be used.



#Article: The implications of Method Placement on API Learnability
Study the method placement in APIs. Shows that method placement can have large usability impact in OOP APIs.

###Description
It was found that method placement — on which class or classes a method is placed — can have large usability impact in object-oriented APIs. 
This was because programmers often start their exploration of an API from one "main" object, and were slower finding other objects that were not referenced in the methods of the main object. 

For example, while mailServer.send(mailMessage) might make sense, if programmers often begin their API explorations from the MailMessage class, then this makes it harder to find the MailServer class than the alternative mailMessage.send(mailServer).

```
mailServer.send(mailMessage) 
vs
mailMessage.send(mailServer)
```

###Conclusion
The study shows that programmers were faster using APIs in which the classes from which they started their exploration included references to the other classes they needed.



#Article: Usability Implication of Requiring Parameters in Objects' Constructors
Study the use of required parameters in constructors. (create-set-call vs required constructor)
Turns on, constructors without required parameters (create-set-call) are easier to use.
###Description
```
//Default constructor ("Create-set-call")
var foo = new FooClass();
foo.Bar = barValue;
foo.Use();

//Required constructor
var foo = new FooClass(varValue);
foo.Use();
```
###Conclusion
Based on a study of 30 programmers of three different personas, we have found that APIs that required constructor parameters did not prevent errors as expected and that APIs that instead used the createset-call pattern of object construction were more usable.  



#Article: Useful, but usable? Factors Affecting the Usability of APIs
Study about the actual impact of each usability factor.

###API Usability Factors
| Index | Usability Factor | Description |
| --- | --- | --- |
| f-01 | Complexity | Increased size and complexity of the exposed features, concept, and architecture reduce usability. |
| f-02 | Naming | Convention followed in the naming of interface level functions and variables. Descriptive names are preferable to abbreviate names. |
| f-03 | Caller’s perspective | Explicitly how the caller will invoke functions or features should be clear/intuitive to the user for better usability. |
| f-04 | Documentation | Complete, clear, and up to date documentation and examples of usage increase usability. |
| f-05 | Consistency | Consistency in the design and adherence with common conventions increase usability. |
| f-06 | Conceptual correctness | Conceptual correctness in the design and naming of features is important for usability. |
| f-07 | Parameter and return | The number and types of parameters to functions and the return types have signiﬁcant impact on usability. Too many parameters reduce usability. |
| f-08 | Constructor parameter | The default (parameterless) constructor is often easier than parameterized constructor to instantiate objects, specially to the beginners and intermediate programmers. |
| f-09 | Factory pattern vs. constructor | Programmers naturally expect constructor to instantiate object, rather than factory methods. Instantiating objects through factory methods sometimes cause difﬁculty. |
| f-10 | Data types | Types of the exposed objects and attributes. Data types should be chosen properly to avoid unnecessary type-casting, resource consumption, and loss of precision. |
| f-11 | Use of attributes | Dispersion and functional dependencies of attributes. Cohesive implementation of functionality increases usability. |
| f-12 | Concurrency | Proper implementation of concurrency and exposer of mutable elements. Unnecessary exposer of mutable elements may raise thread-safety issues and increase pitfalls for misuse. |
| f-13 | Error handling | Mechanism for error prevention by information hiding, as well as proper handling of error conditions through diagnosis information and mechanism for recovery. |
| f-14 | Leftovers for client | Availability of ready implementation of what the users may need reduces the users’ overhead. |
| f-15 | Multiple ways to do one thing | Availability of multiple ways (e.g., several methods offering the same functionality) to do the same thing may puzzle the users in choosing from the alternatives. |
| f-16 | Reference chain | Long chain of method calls or inheritance hierarchy are difﬁcult to track, and reduce usability. |
| f-17 | Implementation vs. interface dependency | Interface dependencies between components provide more ﬂexibility and so those are recommended over implementation dependencies. |
| f-18 | Memory management | Memory management (allocation and deallocation of memory) responsibilities left to the user reduces API usability. |
| f-19 | Technical mismatch | Compatibility with the platform and other technologies in the functional environment is important for usability. |
| f-20 | API change | Backward compatibility is needed for usability, while deprecation of common features may surprise users. |
| f-21 | API aging | API aging occurs when the target platform changes but the API fails to keep pace with the platform evolution, and consequently becomes unusable API. |
| f-22 | Code intelligibility | Readability of the client code affects maintainability. |