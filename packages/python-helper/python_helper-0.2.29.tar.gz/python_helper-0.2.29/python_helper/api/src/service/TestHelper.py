from python_helper.api.src.annotation import TestAnnotation
from python_helper.api.src.annotation.TestAnnotation import Test
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import SettingHelper, LogHelper, ReflectionHelper, ObjectHelper, StringHelper
import time

PY = 'py'
DOT_PY = f'{c.DOT}{PY}'
TEST_SUFIX_NAME = 'Test'
TEST_DOT_PY = f'{TEST_SUFIX_NAME}{DOT_PY}'
TEST_PACKAGE = TEST_SUFIX_NAME.lower()

GLOBALS_INSTANCE_LIST = []
RESULTS = {}
TEST_KWARGS = {
    'argsOfCallBefore' : [GLOBALS_INSTANCE_LIST],
    'argsOfCallAfter' : [GLOBALS_INSTANCE_LIST],
    'returns' : RESULTS
}

def getTestEnvironmentVariables(globalsInstance) :
    return {
        LogHelper.LOG : globalsInstance.logStatus,
        LogHelper.SUCCESS : globalsInstance.successStatus,
        LogHelper.SETTING : globalsInstance.settingStatus,
        LogHelper.DEBUG : globalsInstance.debugStatus,
        LogHelper.WARNING : globalsInstance.warningStatus,
        LogHelper.FAILURE : globalsInstance.failureStatus,
        LogHelper.WRAPPER : globalsInstance.wrapperStatus,
        LogHelper.ERROR : globalsInstance.errorStatus,
        LogHelper.TEST : globalsInstance.testStatus
    }

def getGlobalsTestKwargs(inspectGlobals, globalsInstance) :
    import globals
    TEST_KWARGS['callBefore'] = globals.runBeforeTest
    TEST_KWARGS['callAfter'] = globals.runAfterTest
    TEST_KWARGS['inspectGlobals'] = inspectGlobals
    TEST_KWARGS['kwargsOfCallBefore'] = {
        'muteLogs' : not inspectGlobals,
        'logLevel' : LogHelper.DEBUG
    }
    TEST_KWARGS['kwargsOfCallAfter'] = {
        'muteLogs' : not inspectGlobals,
        'logLevel' : LogHelper.DEBUG
    }
    return {
        'logResult' : False,
        'environmentVariables' : getTestEnvironmentVariables(globalsInstance),
        **TEST_KWARGS
    }

def updateTestNames(testNames, queryResult) :
    if not c.NOTHING == queryResult :
        for key, value in queryResult.items() :
            if c.NOTHING == value and key.endswith(TEST_DOT_PY) :
                testNames.append(key[:-len(DOT_PY)])
            else :
                updateTestNames(testNames, value)

def isTestToRun(testModule, attributeData, runSpecificTests, testsToRun) :
    return (
            not runSpecificTests or
            (runSpecificTests and f'{ReflectionHelper.getName(testModule)}{c.DOT}{attributeData[1]}' in testsToRun)
        ) and ReflectionHelper.getAttributeOrMethod(attributeData[0], TestAnnotation.IS_TEST_METHOD, muteLogs=True)

def getTestNames(testQueryTree) :
    testNames = []
    for queryResultKey, queryResult in testQueryTree.items() :
        LogHelper.prettyPython(getTestNames, 'Query result', queryResult, logLevel=LogHelper.TEST)
        updateTestNames(testNames, queryResult)
    return testNames

def getUnitTest(inspectGlobals, globalsInstance) :
    @Test(**getGlobalsTestKwargs(inspectGlobals, globalsInstance))
    def unitTest(testModule, testName, data, testReturns, logResult) :
        discountTimeEnd = time.time()
        if logResult :
            LogHelper.test(unitTest, f'Sinlge {testName}{c.DOT}{data[1]} started')
        moduleTestStartTime = time.time()
        testReturns[data[1]] = data[0]()
        if logResult :
            LogHelper.test(unitTest, f'Single {testName}{c.DOT}{data[1]} completed in {time.time() - moduleTestStartTime} seconds')
        someDidRun = True
        return testName, data, testReturns, someDidRun, logResult, discountTimeEnd
    return unitTest

def getUnitTestBatch(inspectGlobals, globalsInstance) :
    @Test(**getGlobalsTestKwargs(inspectGlobals, globalsInstance))
    def unitTestBatch(testModule, data) :
        discountTimeEnd = time.time()
        data[0]()
        return discountTimeEnd
    return unitTestBatch

def getModuleTest(inspectGlobals, logResult, globalsInstance) :
    @Test(**getGlobalsTestKwargs(inspectGlobals, globalsInstance))
    def tddModule(testName, testModule, dataList, times, runSpecificTests, testsToRun, allShouldRun, someShouldRun, logResult) :
        import globals
        tddModuleGlobalsInstance = globals.newGlobalsInstance(testModule.__file__
            , successStatus = globalsInstance.successStatus
            , errorStatus = globalsInstance.errorStatus
            , settingStatus = globalsInstance.settingStatus or inspectGlobals
            , debugStatus = globalsInstance.debugStatus
            , warningStatus = globalsInstance.warningStatus
            , wrapperStatus = globalsInstance.wrapperStatus
            , testStatus = globalsInstance.testStatus
            , logStatus = globalsInstance.logStatus
        )
        originalLogEnvs = {**LogHelper.LOG_HELPER_SETTINGS}
        LogHelper.test(tddModule, f'{testName} started')
        testReturns = {}
        testTime = 0
        for data in dataList :
            testMustRun = isTestToRun(testModule, data, runSpecificTests, testsToRun)
            LogHelper.prettyPython(tddModule, f'test attribute or method', data[0], logLevel=LogHelper.TEST)
            LogHelper.prettyPython(tddModule, f'isTestToRun', testMustRun, logLevel=LogHelper.TEST)
            if testMustRun :
                for index in range(times) :
                    originalEnvironmentVariables, originalActiveEnvironment = SettingHelper.replaceEnvironmentVariables(originalLogEnvs)
                    testTimeStart = time.time()
                    if times - 1 == index :
                        runnableUnitTest = getUnitTest(inspectGlobals, globalsInstance)
                        testName, data, testReturns, someDidRun, logResult, discountTimeEnd = runnableUnitTest(testModule, testName, data, testReturns, logResult)
                    else :
                        runnableUnitTestBatch = getUnitTestBatch(inspectGlobals, globalsInstance)
                        discountTimeEnd = runnableUnitTestBatch(testModule, data)
                    testTime += time.time() - discountTimeEnd
                    SettingHelper.recoverEnvironmentVariables(originalLogEnvs, originalEnvironmentVariables, originalActiveEnvironment)
            else :
                allDidRun = False
        if not allShouldRun == allDidRun and someShouldRun == someDidRun :
            amountAlthought = getAmmount(allShouldRun, someShouldRun)
            shouldOrShouldnt = getShouldOrShouldntAsString(allShouldRun, someShouldRun)
            amountAfterAlthought = getAmmount(allDidRun, someDidRun)
            didOrDidnt = getSomeDidOrDidntAsString(allDidRun, someDidRun)
            errorMessage = f'Inconsistenc{StringHelper.getS(allShouldRun or someShouldRun, es=True)} detected. Although {amountAlthought} test{StringHelper.getS(allShouldRun or someShouldRun)} {shouldOrShouldnt} run, {amountAfterAlthought} {didOrDidnt} run'
            exception = Exception(errorMessage)
            raise exception
        return allDidRun, someDidRun, testTime, testReturns
    return tddModule

def runModuleTests(testName, runnableTddModule, times, runSpecificTests, testsToRun, logResult, globalsInstance) :
    import globals
    testModule = globals.importModule(testName)
    dataList = ReflectionHelper.getAttributeDataList(testModule)
    LogHelper.prettyPython(runnableTddModule, f'{ReflectionHelper.getName(testModule)} tests loaded', dataList, logLevel=LogHelper.TEST)
    allShouldRun, someShouldRun, allDidRun, someDidRun = getRunStatus(testModule, dataList, runSpecificTests, testsToRun)
    testReturns = {}
    testTime = 0
    totalTestTimeStart = time.time()
    if someShouldRun :
        defaultMessage = f'{testName}{StringHelper.getS(allShouldRun)}'
        methodReturnException = None
        LogHelper.printTest(f'{defaultMessage} started', condition=logResult, newLine=False, margin=False)
        try :
            allDidRun, someDidRun, testTime, testReturns = runnableTddModule(testName, testModule, dataList, times, runSpecificTests, testsToRun, allShouldRun, someShouldRun, logResult)
            LogHelper.printTest(f'{defaultMessage} succeed. {getTestRuntimeInfo(times, testTime, time.time() - totalTestTimeStart)}', condition=logResult, newLine=False, margin=False)
        except Exception as exception :
            methodReturnException = exception
            LogHelper.printError(f'{defaultMessage} failed', condition=True, newLine=False, margin=False, exception=methodReturnException)
        exceptionRaised = ObjectHelper.isNotNone(methodReturnException)
        defaultMessage = f'{testName}{StringHelper.getS(not exceptionRaised and allDidRun)}'
        if exceptionRaised :
            raise methodReturnException
    return allDidRun, someDidRun, testTime, testReturns

def getRunStatus(testModule, dataList, runSpecificTests, testsToRun) :
    allDidRun = True
    someDidRun = False
    allShouldRun = True
    someShouldRun = False
    for data in dataList :
        if isTestToRun(testModule, data, runSpecificTests, testsToRun) :
            someShouldRun = True
        else :
            allShouldRun = False
    allShouldRun, someShouldRun, allDidRun, someDidRun
    return allShouldRun, someShouldRun, allDidRun, someDidRun

def getAmmount(allShouldRun, someShouldRun) :
    if allShouldRun :
        return 'all'
    elif someShouldRun :
        return 'some'
    else :
        return 'none'

def getShouldOrShouldntAsString(allShouldRun, someShouldRun) :
    return f'should' if allShouldRun or someShouldRun else f'shouldn{c.SINGLE_QUOTE}t'

def getSomeDidOrDidntAsString(allDidRun, someDidRun) :
    if allDidRun :
        return 'all'
    elif someDidRun :
        return 'some'
    else :
        return 'none'

def getSomeDidOrDidntAsString(allDidRun, someDidRun) :
    return 'did' if allDidRun or someDidRun else f'didn{c.SINGLE_QUOTE}t'

def run(
    filePath,
    runOnly = None,
    times = 1,
    successStatus = True,
    errorStatus = True,
    settingStatus = False,
    debugStatus = True,
    warningStatus = True,
    wrapperStatus = False,
    testStatus = False,
    logStatus = False,
    inspectGlobals = False,
    logResult = True
) :
    import globals
    globalsInstance = globals.newGlobalsInstance(filePath
        , successStatus = successStatus
        , errorStatus = errorStatus
        , settingStatus = settingStatus or inspectGlobals
        , debugStatus = debugStatus
        , warningStatus = warningStatus
        , wrapperStatus = wrapperStatus
        , testStatus = testStatus
        , logStatus = logStatus
    )
    testsToRun = [] if ObjectHelper.isNone(runOnly) or ObjectHelper.isNotCollection(runOnly) else runOnly
    runSpecificTests = ObjectHelper.isNotEmpty(testsToRun)
    returns = {}
    LogHelper.prettyPython(run, f'runSpecificTests: {runSpecificTests}, testsToRun', testsToRun, logLevel=LogHelper.TEST)
    testQueryTree = SettingHelper.querySetting(TEST_PACKAGE, globalsInstance.apiTree)
    LogHelper.prettyPython(run, 'Test query tree', testQueryTree, logLevel=LogHelper.TEST)
    testNames = getTestNames(testQueryTree)
    LogHelper.prettyPython(run, 'Test names', testNames, logLevel=LogHelper.TEST)
    totalTestTimeStart = time.time()
    testTime = 0
    for testName in testNames :
        runnableTddModule = getModuleTest(inspectGlobals, logResult, globalsInstance)
        allDidRun, didRun, moduleTestTime, testReturns = runModuleTests(testName, runnableTddModule, times, runSpecificTests, testsToRun, logResult, globalsInstance)
        returns[testName] = testReturns
        testTime += moduleTestTime
    totalTestTime = time.time() - totalTestTimeStart
    if logResult :
        LogHelper.success(run, f'{globalsInstance.apiName} tests completed. {getTestRuntimeInfo(times, testTime, totalTestTime)}')
    return returns

def getTestRuntimeInfo(times, testTime, totalTestTime) :
    testRuntimeInfo = None
    try :
        testRuntimeInfo = f'It {StringHelper.getToBe(True, singular=1==times, tense=StringHelper.PAST)} {times} test run{StringHelper.getS(times > 1)} in {testTime} seconds. Total test time: {totalTestTime} seconds'
    except Exception as exception :
        LogHelper.warning(getTestRuntimeInfo, 'Not possible do get test runtime info', exception=exception)
        testRuntimeInfo = c.NOTHING
    return testRuntimeInfo
