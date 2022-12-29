# mortal
嘿嘿

## TODO
    1. 记录任务重试次数(done)
    2. controller支持获取运行中任务的日志(需要加上task的信息) (done)
    3. task status监控日志获取时, 即使任务已被删除, 也要返回, 不能过滤掉 (done)
    4. swagger页面全部需要支持nginx代理转发时的处理
    5. task status 与 tasks running 日志 需要加上任务的 开始执行时间 与 结束执行时间(done)
        - actuator schedule 加上任务的 开始执行时间 与 结束执行时间 记录(done)
        - controller返回时的schema调整: 加上任务的 开始执行时间 与 结束执行时间 以及重试次数(done)

## bug fix
    1. 同一个actuator中执行的任务运行日志需要发到topic的一个partition上以保证有序记录日志(done)
