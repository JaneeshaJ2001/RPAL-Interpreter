import ASTNode
import sys
import math
from controlStructure import LambdaExpression, Beta, Tau
from Environment import Environment

class CSEMachine :
    results = []

    def __init__(self , ctrlStructures ,file):
        #Initializes the CSE machine with control structures and a file.

        self.mapEnvironments={}
        self.curEnvIdx=0
        self.maxEnvIdx=0

        self.curEnvStack=[]
        self.file=file

        env=Environment(self.curEnvIdx)
        self.mapEnvironments[self.curEnvIdx]=env
        self.curEnvStack.append(env)


        self.ctrlStructures = ctrlStructures
        self.stack = []
        self.control = []
        self.stack.append(env)
        self.control.append(env)
        self.control.extend(ctrlStructures[0])


    def binOp(self ,op, rand1,rand2):
        #Performs binary operations on operands.

        binop_type=op.type
        if isinstance(rand2 , ASTNode.ASTNode) and isinstance(rand1 ,ASTNode.ASTNode):
            type1=rand1.type
            type2=rand2.type
            val1=rand1.value
            val2=rand2.value

        if binop_type == "+":
            result = ASTNode.ASTNode("TokenType.INT")
            result.value = str(int(val1) + int(val2))
            return result

        elif binop_type == "-":
            result=ASTNode.ASTNode( "TokenType.INT")
            result.value=str(int(val1) -int(val2))
            return result

        elif binop_type == "*":
            result= ASTNode.ASTNode(  "TokenType.INT" )
            result.value=str(int(val1 )* int(val2))
            return result
        elif binop_type == "/":

            result=ASTNode.ASTNode("TokenType.INT")
            result.value=str(val1 // val2)

            return result
        elif binop_type == "**":
            result = ASTNode.ASTNode("TokenType.INT")
            result.value = str( math.pow(int(val2) ,int(val1)))
           
            return result


        elif binop_type == "&":
            
            result=""
            if val1 == "true" and val2 == "true":
                result = ASTNode.ASTNode("true")
                result.value = "true"
            else:
                result = ASTNode.ASTNode("false")
                result.value = "false"
            return result

        elif binop_type == "or":
            result=""
            if val1 == "true" and val2 == "true":
                result = ASTNode.ASTNode("true")
                result.value = "true"
            elif  val1 == "false" and val2 == "true":
                result = ASTNode.ASTNode("true")
                result.value = "true"

            elif  val1 == "true" and val2 == "false":
                result = ASTNode.ASTNode("true")
                result.value = "true"
            else:             
                result = ASTNode.ASTNode("false")
                result.value = "false"
         
            return result


        elif binop_type == "aug":
          
            if isinstance(rand1, list):
                if isinstance(rand2, list):
                    
                    t1 = rand1
                    t2 = rand2
                    t2Size = len(t2)
                    for i in range(t2Size):
                        t1.append(t2[i])
                    return t1
                else:
                    if isinstance(rand2, ASTNode.ASTNode):
                        
                        t1 = rand1
                        t1.append(rand2)
                        return t1
                    else:
                        
                        exit(-1)
            elif rand1.value == "nil":
                if isinstance(rand2, list):
                    return rand2
                else:
                    if isinstance(rand2, ASTNode.ASTNode):
                        
                        t = []
                        t.append(rand2)
                        return t
                    else:
                        exit(-1)
            else:
               
                exit(-1)
        elif binop_type == "gr" or  binop_type == ">" :

            if float(val1)>float(val2):
                result = ASTNode.ASTNode("true")
                result.value = "true"
            else :
                result = ASTNode.ASTNode("false")
                result.value = "false"
            return  result

        elif binop_type == "ge" or  binop_type == ">=":

            if int(val1) >= int(val2):
                result = ASTNode.ASTNode("true")
                result.value = "true"
            else:
                result = ASTNode.ASTNode("false")
                result.value = "false"
            return  result

        elif binop_type == "ls" or  binop_type == "<":

            if int(val1) < int(val2):
                result = ASTNode.ASTNode("true")
                result.value = "true"
            else:
                result = ASTNode.ASTNode("false")
                result.value = "false"
            return  result

        elif binop_type == "le" or  binop_type == "<=":

            if int(val1) <= int(val2):
                result = ASTNode.ASTNode("true")
                result.value = "true"
            else:
                result = ASTNode.ASTNode("false")
                result.value = "false"
            return  result

        elif binop_type == "ne":

            result = None

            if rand1.type == "TokenType.STRING" and rand2.type == "TokenType.STRING":

                if val1 != val2:
                    result = ASTNode.ASTNode("true")
                    result.value = "true"

                else:
                    result = ASTNode.ASTNode("false")
                    result.value = "false"

                return result

            else:
                if (int(val1) != int(val2)):
                    result = ASTNode.ASTNode("true")
                    result.value = "true"

                else:
                    result = ASTNode.ASTNode("false")
                    result.value = "false"
        
            return result


        elif binop_type == "eq":
            
            result=None
            if rand1.type == "TokenType.STRING" and rand2.type == "TokenType.STRING":
                if val1 == val2:
                    result = ASTNode.ASTNode("true")
                    result.value = "true"
                else:
                    result = ASTNode.ASTNode("false")
                    result.value = "false"
                return result
            else :

                if  (float(val1) == float(val2)):

                    result=ASTNode.ASTNode("true")
                    result.value="true"
                else:
                    result=ASTNode.ASTNode("false")
                    result.value="false"
            
            return result

        else:
            print("no matching binary operator found:", binop_type)

        print("Error: Unexpected condition encountered.")
        return None

    def unaryOp(self, op, rand):
        #Performs unary operations on operands.

        unop_type=op.type
        type1=rand.type
        val1=rand.value
        if unop_type == "not":
            if type1 != "true" and type1 != "false":
                print("Wrong type: true/false expected for operand: type1:", type1)
                exit(-1)
            if val1 == "true":
                result=ASTNode.ASTNode("false")
                result.value="false"

                return result
            else:
                result = ASTNode.ASTNode("true")
                result.value = "true"

                return result
        if unop_type == "neg":
            if type1 != "TokenType.INT":
                print("Wrong type: INT expected for operand: type1:", type1)
                exit(-1)

            result=ASTNode.ASTNode("TokenType.INT")
            result.value= str(-int(val1))
            return result

        print("no matching unary operator found:", unop_type)
        return None


    def Print(self ,obj):

        if isinstance( obj , ASTNode.ASTNode):
            string = obj.value
            if isinstance(obj.value,str):
                if "\\n" in string:
                    string=string.replace("\\n","\n")
                if "\\t" in string:
                    string=string.replace("\\t","\t")


            print(string ,end="")
           

        if isinstance(obj ,list):
            print("(",end="")
            for index ,i in enumerate(obj) :
                self.Print(i)
                if index < len(obj)-1:
                    print(",",end=" " )
                
            print(")",end="\n")

            
    def execute(self):
        #Executes the control structures.

        count = 0
        while len(self.control)>0:
            # Implement execution logic here...
            
            controlTop=self.control[-1]
            stackTop=self.stack[-1]

            
            if isinstance(controlTop, LambdaExpression):
                lambdha=self.control.pop(-1)
                lambdha.envIdx=self.curEnvIdx
                self.stack.append(lambdha)

            elif isinstance(controlTop, ASTNode.ASTNode):
                
                node=controlTop
                
                if node.type=="gamma":
                    if isinstance(stackTop, LambdaExpression):
                        self.control.pop()  # remove gamma
                        self.stack.pop()  # remove lambda

                        rand = self.stack[-1] # get rand from stack
                        self.stack.pop()  # remove rand from stack

                        lambdaStack = stackTop
                        k = lambdaStack.lambdaIdx
                        envIdLambda = lambdaStack.envIdx
                        tokenStackLambdaList = None
                        tokenStackLambda = None


                        if isinstance(lambdaStack.item, ASTNode.ASTNode):
                            tokenStackLambda = lambdaStack.item  # the variable of lambda of stack
                        else:
                            if isinstance(lambdaStack.item, list):
                                tokenStackLambdaList = lambdaStack.item
                            else:
                                print("tokenStackLambdaList is not a list, some error")

                        
                        self.maxEnvIdx += 1
                        self.curEnvIdx = self.maxEnvIdx
                        env = Environment(self.curEnvIdx)

                        if tokenStackLambdaList is None:
                           
                            env.set_env_params(self.mapEnvironments.get(envIdLambda), tokenStackLambda.value, rand)
                        else:
                        
                            cnt = 0
                            for item in tokenStackLambdaList:
                                env.set_env_params(self.mapEnvironments.get(envIdLambda), item.value,
                                                   rand[cnt])
                                cnt += 1

                        self.control.append(env)
                        self.control.extend(self.ctrlStructures[k]) # k is from stack
                        self.stack.append(env)
                        # maintain environment variables
                        self.curEnvStack.append(env)
                        self.mapEnvironments[self.curEnvIdx] = env
                   
                    elif isinstance(stackTop, Eta):
                        self.control.append(ASTNode.ASTNode("gamma"))
                        eta = stackTop
                        lambdaStack = LambdaExpression(eta.envId, eta.id, eta.tok)
                        self.stack.append(lambdaStack)
                    elif isinstance( stackTop, ASTNode.ASTNode):
                        if stackTop.type == "Y*":

                            self.control.pop(-1)
                            self.stack.pop(-1)
                            lambdaY=self.stack[-1]
                            self.stack.pop(-1)
                            self.stack.append(Eta(lambdaY.envIdx,lambdaY.lambdaIdx,lambdaY.item))
                        elif stackTop.value == "Print":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            rand =self.stack.pop(-1)
                            self.Print(rand)
                            self.stack.append(ASTNode.ASTNode("dummy"))

                        elif stackTop.value == "Conc":
                            self.stack.pop(-1)
                            stackTop =self.stack[-1]
                            str1 = stackTop.value
                            self.stack.pop(-1)
                            str2 = self.stack[-1].value
                            self.stack.pop(-1)  # remove str2
                            str_result =  str2 +str1
                            result=ASTNode.ASTNode("TokenType.STRING")
                            result.value= str_result
                            self.stack.append(result)  # push result into stack

                            self.control.pop(-1)  # remove gamma from control
                            
                            self.control.pop(-1)  # remove gamma from control
                            

                        elif stackTop.value=="Stem":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            str1=self.stack.pop(-1)
                            if len(str1.value) == 0:
                                sys.exit(0)
                            
                            else:
                                value = str1.value[0]
                            result = ASTNode.ASTNode("TokenType.STRING")
                            result.value = value
                            self.stack.append(result)

                        elif stackTop.value=="Stern":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            str1=self.stack.pop(-1)
                            if len(str1.value) == 0:
                                sys.exit(0)
                            if len(str1.value)==1:
                                value=''                                

                            else:                              
                                value=str1.value[1:]
                            result = ASTNode.ASTNode("TokenType.STRING")
                            result.value = value
                            self.stack.append(result)

                        elif stackTop.value== "Null":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            stackTop=self.stack[-1]
                            self.stack.pop(-1)


                            if isinstance(stackTop , ASTNode.ASTNode):
                                if stackTop.type== 'nil':
                                    result=ASTNode("true")
                                    result.value="true"
                                    self.stack.append(result)

                            elif isinstance(stackTop ,list):
                                if len(stackTop) == 0 :
                                    result = ASTNode.ASTNode("true")
                                    result.value = "true"
                                    self.stack.append(result)
                                else:
                                    result = ASTNode.ASTNode("false")
                                    result.value = "false"
                                    self.stack.append(result)

                        elif stackTop.value =="ItoS":
                            self.control.pop(-1)
                            self.stack.pop(-1)

                            stackTop= self.stack.pop(-1)
                            result=ASTNode.ASTNode("TokenType.STRING")
                            result.value=str(stackTop.value)
                            print(result.value)
                            self.stack.append(result)

                        elif stackTop.value == "Isinteger":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop , ASTNode.ASTNode):
                                if stackTop.type=="TokenType.INT":
                                    result=ASTNode.ASTNode("true")
                                    result.value="true"
                                    self.stack.append(result)
                                else:
                                    result = ASTNode.ASTNode("false")
                                    result.value = "false"
                                    self.stack.append(result)
                            else :
                                sys.exit(0)


                        elif stackTop.value == "Istruthvalue":

                            self.control.pop(-1)
                            self.stack.pop(-1)
                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop, ASTNode.ASTNode):

                                if stackTop.type == "true" or stackTop.type=="false":

                                    result = ASTNode.ASTNode("true")
                                    result.value = "true"
                                    self.stack.append(result)

                            else:
                                result = ASTNode.ASTNode("false")
                                result.value = "false"
                                self.stack.append(result)

                        elif stackTop.value== "Isstring" :
                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)

                            if isinstance(stackTop, ASTNode.ASTNode):
                                if stackTop.type == "TokenType.STRING":
                                    result = ASTNode.ASTNode("true")
                                    result.value = "true"
                                    self.stack.append(result)
                                else:
                                    result = ASTNode.ASTNode("false")
                                    result.value = "false"
                                    self.stack.append(result)
                            else:
                                sys.exit(0)

                        elif stackTop.value=="Istuple":
                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)
                            if isinstance(stackTop,list):
                                result = ASTNode.ASTNode("true")
                                result.value = "true"
                                self.stack.append(result)

                            else:
                                result = ASTNode.ASTNode("false")
                                result.value = "false"
                                self.stack.append(result)


                        elif stackTop.value=="Isdummy":
                            self.control.pop(-1)

                            self.stack.pop(-1)

                            stackTop = self.stack.pop(-1)
                            if stackTop.value=="dummy":
                                result = ASTNode.ASTNode("true")
                                result.value = "true"
                                self.stack.append(result)
                            else:
                                result = ASTNode.ASTNode("false")
                                result.value = "false"
                                self.stack.append(result)


                        elif stackTop.value =="Order":
                            self.control.pop(-1)
                            self.stack.pop(-1)
                            rand=self.stack.pop(-1)
                            if isinstance(rand,ASTNode.ASTNode):
                                node = ASTNode.ASTNode("TokenType.INT")
                                node.value="0"

                                self.stack.append(node)
                            elif isinstance(rand, list):
                                node=ASTNode.ASTNode("TokenType.INT")
                                node.value=(len(rand))
                                self.stack.append(node)
                            else:
                                exit(-1)

                        elif stackTop.type=="TokenType.INT":
                            self.control.pop(-1)

                        elif stackTop.type=="TokenType.STRING":
                            self.control.pop(-1)

                    elif isinstance(stackTop, list):
                        self.control.pop(-1)
                        self.stack.pop(-1)
                        index=int(self.stack[-1].value)
                        self.stack.pop(-1)

                        self.stack.append(stackTop[index-1])


                    elif isinstance(stackTop,Eta):
                        self.control.append(ASTNode.ASTNode( "gamma"))
                        eta = stackTop
                        lambdaStack = LambdaExpression(eta.envId, eta.id, eta.tok)
                        self.stack.append(lambdaStack)

                elif node.type in ["-", "+" , "*", "/","or","&","**" ,"aug" ,"gr",">=","ge",">","ls","<","<=","eq","ne","le" ]:
                    op=self.control.pop(-1)
                    rand=self.stack.pop(-1)
                    ran2=self.stack.pop(-1)
                    val=self.binOp(op,rand,ran2 )
                    self.stack.append(val)

                elif node.type=="neg":
                    op = self.control.pop(-1)
                    rand = self.stack.pop(-1)
                    val = self.unaryOp(op, rand)
                    self.stack.append(val)

                elif node.type=="not":
                    op = self.control.pop(-1)
                    rand = self.stack.pop(-1)
                    val = self.unaryOp(op, rand)
                    self.stack.append(val)

                elif node.type=="Y*":

                    Ystar=self.control.pop(-1)
                    self.stack.append(Ystar)

                elif node.type=="TokenType.INT":

                    Ystar = self.control.pop(-1)
                    self.stack.append(Ystar)

                else :
                    
                    self.control.pop()
                    curEnv = self.curEnvStack[-1]
                    type_ = controlTop.type
                    control_value=controlTop.value
                   
                    if controlTop.type == "TokenType.ID":
                       
                        stackVal = curEnv.get_val(controlTop.value)

                        if stackVal is None:
                            curEnv = curEnv.parent
                            while curEnv is not None:
                                stackVal = curEnv.get_val(controlTop.value)
                                if stackVal is not None:
                                    break
                                curEnv = curEnv.parent

                        if stackVal is not None:
                            self.stack.append(stackVal)
                            if isinstance(stackVal, ASTNode.ASTNode):
                                pass
                                
                        if stackVal is None:
                            # if not found in the env tree, check if it was a special function
                            # it may be a special function name which was not redefined
                            if control_value in ["Print", "Conc", "Stern", "Stem", "Order", "Isinteger", "Istruthvalue", "Isstring", "Isinteger", "Istuple", "Isfunction", "Isdummy", "ItoS", "Null"]:
                                # just stack the Print, Stern, Stem, ItoS, Order, conc, may be: aug too
                                # logger.info("pushing into stack : {}".format(type_))
                                self.stack.append(controlTop)
                            else:
                                sys.exit(-1)
                    else:
                        # just put into stack from control
                        self.stack.append(controlTop)



            elif isinstance(controlTop , Tau):
                n = self.control[-1].n

                self.control.pop()
                tuple = []

                while n > 0:
                    tuple.append(self.stack.pop())
                    stackTop = self.stack[-1] if self.stack else None
                    n -= 1
                self.stack.append(tuple)
            elif isinstance(controlTop, Beta):
                if stackTop.type == "true":
                    self.control.pop(-1)  # remove beta
                    self.control.pop(-1)  # remove else
                    self.control.extend(self.ctrlStructures[self.control.pop(-1).idx])
                    self.stack.pop(-1)
                elif stackTop.type == "false":
                    self.control.pop(-1)
                    controlTop = self.control[-1]
                    self.control.pop(-1)  # remove else
                    self.control.pop(-1)  # remove then
                    self.control.extend( self.ctrlStructures[controlTop.idx])  # insert else back
                    self.stack.pop(-1)
            elif isinstance(controlTop, Environment):
                self.control.pop()
                self.stack.pop()
                self.stack.pop()
                self.stack.append(stackTop)
                self.curEnvStack.pop()
               

            count+=1
            
            if (count>500):
                break


class Eta :
    def __init__ (self, envId,id ,tok):
        self.envId=envId
        self.id=id
        self.tok=tok



