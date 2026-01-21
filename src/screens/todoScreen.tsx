import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SocketClient } from '../services/SocketClient';
import { Todo } from '../types/index';
import { styles } from '../styles/styles';
import EditTodoModal from '../components/editTodoModal';

interface TodoScreenProps {
  userId: string;
  onLogout: () => void;
}

const TodoScreen: React.FC<TodoScreenProps> = ({ userId, onLogout }) => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(false);
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    setLoading(true);
    const client = new SocketClient();
    const response = await client.sendAndReceive({
      type: 'getTodos',
      userId,
    });
    setLoading(false);

    if (response.success) {
      setTodos(response.todos);
      updateStats(response.todos);
    } else {
      Alert.alert('Erro', response.error || 'Erro ao carregar tarefas');
    }
  };

  const updateStats = (todoList: Todo[]) => {
    const total = todoList.length;
    const completed = todoList.filter(t => t.done).length;
    setStats({ total, completed, pending: total - completed });
  };

  const addTodo = async () => {
    if (!newTodo.trim()) return;

    const client = new SocketClient();
    const response = await client.sendAndReceive({
      type: 'createTodo',
      userId,
      title: newTodo,
      description: '',
    });

    if (response.success) {
      setNewTodo('');
      loadTodos();
    } else {
      Alert.alert('Erro', response.error || 'Erro ao criar tarefa');
    }
  };

  const toggleTodo = async (todo: Todo) => {
    const client = new SocketClient();
    const response = await client.sendAndReceive({
      type: 'updateTodo',
      todoId: todo.id,
      done: todo.done ? 0 : 1,
    });

    if (response.success) {
      loadTodos();
    } else {
      Alert.alert('Erro', response.error || 'Erro ao atualizar tarefa');
    }
  };

  const editTodo = async (title: string, description: string) => {
    if (!editingTodo) return;

    const client = new SocketClient();
    const response = await client.sendAndReceive({
      type: 'updateTodo',
      todoId: editingTodo.id,
      title,
      description,
    });

    if (response.success) {
      setEditingTodo(null);
      loadTodos();
    } else {
      Alert.alert('Erro', response.error || 'Erro ao atualizar tarefa');
    }
  };

  const deleteTodo = async (todoId: string) => {
    Alert.alert(
      'Confirmar Exclusão',
      'Tem certeza que deseja excluir esta tarefa?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Excluir',
          style: 'destructive',
          onPress: async () => {
            const client = new SocketClient();
            const response = await client.sendAndReceive({
              type: 'deleteTodo',
              todoId,
            });

            if (response.success) {
              loadTodos();
            } else {
              Alert.alert('Erro', response.error || 'Erro ao excluir tarefa');
            }
          },
        },
      ]
    );
  };

  const clearCompleted = () => {
    const completedTodos = todos.filter(t => t.done);
    if (completedTodos.length === 0) {
      Alert.alert('Info', 'Não há tarefas concluídas para remover');
      return;
    }

    Alert.alert(
      'Limpar Concluídas',
      `Deseja remover ${completedTodos.length} tarefa(s) concluída(s)?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Remover',
          style: 'destructive',
          onPress: async () => {
            for (const todo of completedTodos) {
              const client = new SocketClient();
              await client.sendAndReceive({
                type: 'deleteTodo',
                todoId: todo.id,
              });
            }
            loadTodos();
          },
        },
      ]
    );
  };

  const showTodoOptions = (todo: Todo) => {
    Alert.alert(
      'Opções',
      `"${todo.title}"`,
      [
        {
          text: todo.done ? 'Marcar como Pendente' : 'Marcar como Concluída',
          onPress: () => toggleTodo(todo),
        },
        {
          text: 'Editar',
          onPress: () => {
            setEditingTodo(todo);
            setModalVisible(true);
          },
        },
        {
          text: 'Excluir',
          style: 'destructive',
          onPress: () => deleteTodo(todo.id),
        },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  };

  const renderTodo = ({ item }: { item: Todo }) => (
    <TouchableOpacity
      style={styles.todoItem}
      onPress={() => toggleTodo(item)}
      onLongPress={() => showTodoOptions(item)}
    >
      <View style={styles.todoContent}>
        <Text style={[styles.todoText, item.done && styles.todoTextDone]}>
          {item.done ? '✓' : '○'} {item.title}
        </Text>
        {item.description ? (
          <Text style={styles.todoDescription}>{item.description}</Text>
        ) : null}
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Minhas Tarefas</Text>
          <TouchableOpacity onPress={onLogout}>
            <Text style={styles.logoutText}>Sair</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.statsContainer}>
          <Text style={styles.statsText}>Total: {stats.total}</Text>
          <Text style={styles.statsText}>Pendentes: {stats.pending}</Text>
          <Text style={styles.statsText}>Concluídas: {stats.completed}</Text>
        </View>

        {loading ? (
          <ActivityIndicator size="large" style={styles.loader} />
        ) : (
          <FlatList
            data={todos}
            renderItem={renderTodo}
            keyExtractor={item => item.id}
            style={styles.todoList}
            contentContainerStyle={styles.todoListContent}
          />
        )}

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.todoInput}
            placeholder="Nova tarefa..."
            value={newTodo}
            onChangeText={setNewTodo}
            onSubmitEditing={addTodo}
          />
          <TouchableOpacity style={styles.addButton} onPress={addTodo}>
            <Text style={styles.addButtonText}>+</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          style={[styles.button, styles.clearButton]}
          onPress={clearCompleted}
        >
          <Text style={styles.buttonText}>Limpar Concluídas</Text>
        </TouchableOpacity>

        <EditTodoModal
          visible={modalVisible}
          todo={editingTodo}
          onClose={() => {
            setModalVisible(false);
            setEditingTodo(null);
          }}
          onSave={editTodo}
        />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default TodoScreen;