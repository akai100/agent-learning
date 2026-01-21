```InMemorySaver``` 的主要任务是保存 Graph 的 State（状态）。 当你在调用 Graph 时传入一个 ```thread_id```，```InMemorySaver``` 会根据这个 ID 查找之前的快照。

## 存储的值

### 1. 状态值 (State Values)

这是最重要的数据。它保存了你在 ```StateGraph``` 中定义的 ```State``` 字典里的所有键值对。

+ Message History: 所有的对话记录（BaseMessage 对象列表）。

+ Custom Variables: 你自定义的变量（如 user_id、search_queries、is_authenticated 等）。

+ Node Outputs: 每个节点运行后更新到状态中的增量数据。

### 2. 结构化快照 (Checkpoint Metadata)

除了数据本身，它还记录了关于这个状态的“元数据”，用于管理和溯源：

+ Thread ID: 区分不同用户的唯一标识。

+ Checkpoint ID: 每一个步骤生成的唯一 ID（用于回滚）。

+ Parent ID: 指向当前步骤的上一个状态 ID，从而形成一条版本链。

+ Timestamp: 该状态保存的时间。

### 3. 下一步任务 (Next Tasks)

它还保存了图的执行位置：

+ Pending Tasks: 哪些节点已经运行完，哪些节点准备运行。

+ Interrupts: 如果你设置了 interrupt_before（人工介入），它会保存当前停留在哪个节点之前，等待用户的输入。
